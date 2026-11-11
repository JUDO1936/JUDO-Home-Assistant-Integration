"""Protocol and integration contract tests; HA is stubbed, not installed."""
import asyncio
from datetime import datetime, timezone
import importlib
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def module(name, **attrs):
    obj = ModuleType(name)
    obj.__dict__.update(attrs)
    sys.modules[name] = obj
    return obj


class Entity:
    available = True
    def async_write_ha_state(self): pass


class CoordinatorEntity:
    def __class_getitem__(cls, key): return cls
    def __init__(self, coordinator): self.coordinator = coordinator
    @property
    def available(self): return True


class DataUpdateCoordinator:
    def __class_getitem__(cls, key): return cls
    def __init__(self, hass, **kwargs): self.hass = hass
    def async_set_updated_data(self, data): self.data = data


class UpdateFailed(Exception): pass
class HomeAssistantError(Exception): pass

module('homeassistant')
module('homeassistant.components')
for component, base in [('sensor', 'SensorEntity'), ('select', 'SelectEntity'), ('button', 'ButtonEntity'), ('number', 'NumberEntity')]:
    module(f'homeassistant.components.{component}', **{base: Entity},
           SensorDeviceClass=SimpleNamespace(TEMPERATURE='temperature'),
           SensorStateClass=SimpleNamespace(TOTAL_INCREASING='total_increasing', MEASUREMENT='measurement'),
           NumberMode=SimpleNamespace(SLIDER='slider', BOX='box'))
module('homeassistant.const', UnitOfTime=SimpleNamespace(DAYS='d'), UnitOfTemperature=SimpleNamespace(CELSIUS='°C'), UnitOfVolume=SimpleNamespace(CUBIC_METERS='m³'))
module('homeassistant.config_entries', ConfigEntry=object)
module('homeassistant.core', HomeAssistant=object)
module('homeassistant.exceptions', HomeAssistantError=HomeAssistantError)
module('homeassistant.helpers')
module('homeassistant.helpers.entity', EntityCategory=SimpleNamespace(DIAGNOSTIC='diagnostic'))
module('homeassistant.helpers.entity_platform', AddEntitiesCallback=object)
module('homeassistant.helpers.restore_state', RestoreEntity=type('RestoreEntity', (), {}))
module('homeassistant.helpers.update_coordinator', CoordinatorEntity=CoordinatorEntity, DataUpdateCoordinator=DataUpdateCoordinator, UpdateFailed=UpdateFailed)

prefix='custom_components.judo_isoft_pro.'
models=importlib.import_module(prefix+'models')
protocol=importlib.import_module(prefix+'protocol')
const=importlib.import_module(prefix+'const')
api_mod=importlib.import_module(prefix+'api')
coord=importlib.import_module(prefix+'coordinator')
platforms={name: importlib.import_module(prefix+name) for name in ['sensor','number','select','button']}


class FakeApi:
    host='192.168.1.50'
    port=80
    def __init__(self, code): self.code=code; self.reads=[]; self.writes=[]; self.fail=False
    async def read(self, command):
        self.reads.append(command)
        if self.fail: raise api_mod.JudoApiError('offline')
        return {'FF':f'{self.code:02X}', '23':'00', '01':'0C0001', '51':'0600', '57':'14', '3E':'28', '3F':'C409', '40':'F401', '56':'F7A302001700' if self.code in (0x69,0x6E) else 'F6541100', '6900':'00070000380406001200190000000000'}.get(command,'06000000')
    async def write(self, command, data): self.writes.append((command,data)); return ''


class ProtocolTests(unittest.TestCase):
    def test_all_documented_device_ids(self):
        self.assertEqual(set(models.DEVICE_PROFILES), {0x32,0x53,0x43,0x54,0x33,0x57,0x42,0x67,0x58,0x4B,0x4C,0x6E,0x69})
        for code,p in models.DEVICE_PROFILES.items():
            with self.subTest(code=code): self.assertEqual(models.profile_from_hex(f'{code:02x}'),p)
    def test_unknown_and_invalid_types(self):
        for raw in ['','GG','34','5800']:
            with self.subTest(raw=raw), self.assertRaises(ValueError): models.profile_from_hex(raw)
    def test_classic_salt(self):
        self.assertEqual(models.decode_salt('f6541100',models.DEVICE_PROFILES[0x32]),(21750,17))
    def test_xl_salt(self):
        self.assertEqual(models.decode_salt('F7A302001700',models.DEVICE_PROFILES[0x69]),(173047,23))
    def test_invalid_salt_not_zero(self):
        for raw in ['',None,'xyz','FFFF','F65411000000']:
            self.assertIsNone(models.decode_salt(raw,models.DEVICE_PROFILES[0x58]))
    def test_live_status(self):
        s=protocol.decode_6900('000000003804060012001900BA010C00')
        self.assertEqual((s.current_water_flow_l_h,s.current_draw_duration_min,s.current_water_amount_l,s.current_water_temperature_c),(1080,6,18,25))
        self.assertIsNone(protocol.decode_6900('bad'))
    def test_leakage_disabled(self): self.assertEqual(protocol.leakage_status_label(0),'Deaktiviert')
    def test_duration_byte_range(self): self.assertTrue(all(0<=x<=255 for x in const.MAX_DRAW_DURATION_NAME_TO_VALUE.values()))


class IntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def make(self, code):
        api=FakeApi(code)
        c=coord.JudoCoordinator(SimpleNamespace(),api,'Testgerät')
        c.schedule_recheck=lambda command: None
        c.data=await c._async_update_data()
        return c
    async def entities(self,c,platform):
        result=[]
        hass=SimpleNamespace(data={const.DOMAIN:{'test':c}})
        await platforms[platform].async_setup_entry(hass,SimpleNamespace(entry_id='test'),result.extend)
        return result
    async def test_poll_sets_and_no_legacy_status(self):
        for code,p in models.DEVICE_PROFILES.items():
            with self.subTest(code=code):
                c=await self.make(code)
                self.assertEqual(set(c.api.reads),set(p.read_commands))
                await c.async_poll_6900()
                self.assertEqual('6900' in c.api.reads,p.live_status)
    async def test_platform_counts_by_family(self):
        for code,expected in [(0x32,(10,2,1,3)),(0x33,(10,2,1,3)),(0x58,(16,5,4,5)),(0x69,(15,2,1,3))]:
            c=await self.make(code)
            for name,count in zip(platforms,expected):
                with self.subTest(code=code,platform=name): self.assertEqual(len(await self.entities(c,name)),count)
    async def test_classic_buttons_are_alarm(self):
        c=await self.make(0x32)
        buttons=await self.entities(c,'button')
        self.assertEqual({e._attr_name for e in buttons},{'Regeneration starten','Leckagealarm setzen','Leckagealarm zurücksetzen'})
        for e in buttons: await e.async_press()
        self.assertEqual(set(c.api.writes),{('35','00'),('3C',''),('3D','')})
    async def test_xl_salt_sensor(self):
        c=await self.make(0x69)
        sensors=await self.entities(c,'sensor')
        by_name={e._attr_name:e for e in sensors}
        self.assertEqual(by_name['Salzgewicht'].native_value,173.05)
        self.assertEqual(by_name['Salzreichweite'].native_value,23)
    async def test_xl_units(self):
        c=await self.make(0x69)
        select=(await self.entities(c,'select'))[0]
        self.assertEqual(select._attr_options,['°dH','°fH','ppm','mmol'])
        with self.assertRaises(ValueError): await select.async_select_option('°eH')
    async def test_disallowed_write_never_sent(self):
        c=await self.make(0x32)
        for cmd in ['36','41','3F']:
            with self.assertRaises(api_mod.JudoApiError): await c.async_write_command(cmd,'00')
        self.assertEqual(c.api.writes,[])
    async def test_pro_action_payloads(self):
        c=await self.make(0x58)
        c.set_scene_selection('2','0200');c.set_holiday_days(5)
        for e in await self.entities(c,'button'):
            if e._attr_name in ['Szene aktivieren','Urlaubsmodus starten']: await e.async_press()
        self.assertEqual(c.api.writes,[('36','020200'),('41','0105')])
    async def test_hardness_payload_and_unit_guard(self):
        c=await self.make(0x58)
        number=next(e for e in await self.entities(c,'number') if e._attr_name=='Wunschwasserhärte')
        await number.async_set_native_value(7)
        self.assertEqual(c.api.writes,[('30','07')])
        c._cache['23']='04'
        self.assertFalse(number.available)
        with self.assertRaises(ValueError): await number.async_set_native_value(7)
    async def test_initial_unknown_type(self):
        c=coord.JudoCoordinator(SimpleNamespace(),FakeApi(0x34),'Unsupported')
        with self.assertRaises(UpdateFailed): await c._async_update_data()
        self.assertEqual(c.api.reads,['FF'])
    async def test_malformed_read_is_not_cached(self):
        c=await self.make(0x58)
        async def bad_read(command): return ""
        c.api.read=bad_read
        saved=dict(c._cache)
        with self.assertRaises(UpdateFailed): await c._async_update_data()
        self.assertEqual(c._cache,saved)

    async def test_outage_keeps_cache_and_reports_failure(self):
        c=await self.make(0x58);saved=dict(c._cache);c.api.fail=True
        with self.assertRaises(UpdateFailed): await c._async_update_data()
        self.assertEqual(c._cache,saved)


class Response:
    status=200
    async def text(self): return '{"data":"58"}'
    async def json(self,**kw): return {'data':'58'}
    async def __aenter__(self): return self
    async def __aexit__(self,*args): pass


class Session:
    def __init__(self, fail=False): self.urls=[]; self.fail=fail
    def get(self,url,**kw):
        self.urls.append(url)
        if self.fail: raise asyncio.TimeoutError()
        return Response()


class ApiTests(unittest.IsolatedAsyncioTestCase):
    async def test_write_path_and_read_path(self):
        session=Session();api=api_mod.JudoApi(session,'host',80,'admin','password')
        async def no_wait(): pass
        api._wait_for_request_slot=no_wait
        await api.read('FF');await api.write('35','00')
        self.assertEqual(session.urls,['http://host:80/api/rest/FF00','http://host:80/api/rest/350000'])
    async def test_write_timeout_not_retried(self):
        session=Session(True);api=api_mod.JudoApi(session,'host',80,'admin','password')
        async def no_wait(): pass
        api._wait_for_request_slot=no_wait
        with self.assertRaises(api_mod.JudoApiError): await api.write('35','00')
        self.assertEqual(len(session.urls),1)
    async def test_read_timeout_retried(self):
        session=Session(True);api=api_mod.JudoApi(session,'host',80,'admin','password')
        async def no_wait(): pass
        api._wait_for_request_slot=no_wait
        with self.assertRaises(api_mod.JudoApiError): await api.read('FF')
        self.assertEqual(len(session.urls),2)
    async def test_invalid_hex_never_requested(self):
        session=Session();api=api_mod.JudoApi(session,'host',80,'admin','password')
        with self.assertRaises(api_mod.JudoApiError): await api.write('ZZ','00')
        self.assertEqual(session.urls,[])

if __name__=='__main__': unittest.main()
