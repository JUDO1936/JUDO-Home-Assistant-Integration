"""Device capabilities taken from the supplied RESTAPI_Kommandos.pdf.

Keep this module independent of Home Assistant so protocol rules are testable.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceProfile:
    name: str
    family: str
    salt_weight_bytes: int = 2

    @property
    def live_status(self) -> bool:
        return self.family in {"pro", "xl"}

    @property
    def scenes(self) -> bool:
        return self.family == "pro"

    @property
    def limits(self) -> bool:
        # PRO explicitly documents readback and unambiguous units. The older
        # tables interchange the labels/units of 3F and 40; do not guess.
        return self.family == "pro"

    @property
    def alarm_only(self) -> bool:
        return self.family == "classic"

    @property
    def hardness_units(self) -> tuple[str, ...]:
        return ("0", "2", "4", "5") if self.family == "xl" else tuple(str(i) for i in range(7))

    @property
    def read_commands(self) -> tuple[str, ...]:
        common = ("FF", "06", "01", "51", "23", "56", "57", "28", "29", "25")
        return common + (("3E", "3F", "40") if self.limits else ())

    @property
    def write_commands(self) -> frozenset[str]:
        common = {"30", "24", "57", "35", "3C", "3D"}
        if self.scenes:
            common |= {"36", "41", "3E", "3F", "40"}
        return frozenset(common)


DEVICE_PROFILES = {
    0x32: DeviceProfile("i-soft", "classic"),
    0x53: DeviceProfile("i-soft", "classic"),
    0x43: DeviceProfile("i-soft K", "classic"),
    0x54: DeviceProfile("i-soft K", "classic"),
    0x33: DeviceProfile("i-soft SAFE+", "safe"),
    0x57: DeviceProfile("i-soft SAFE+", "safe"),
    0x42: DeviceProfile("i-soft K SAFE+", "safe"),
    0x67: DeviceProfile("i-soft K SAFE+", "safe"),
    0x58: DeviceProfile("i-soft PRO", "pro"),
    0x4B: DeviceProfile("i-soft PRO", "pro"),
    0x4C: DeviceProfile("i-soft PRO L", "pro"),
    0x6E: DeviceProfile("i-soft PRO XL 70", "xl", 4),
    0x69: DeviceProfile("i-soft PRO XL 140", "xl", 4),
}


def profile_from_hex(raw: str) -> DeviceProfile:
    data = bytes.fromhex(raw)
    if len(data) != 1 or data[0] not in DEVICE_PROFILES:
        raise ValueError("Unsupported i-soft device type")
    return DEVICE_PROFILES[data[0]]


def decode_salt(raw: str | None, profile: DeviceProfile) -> tuple[int, int] | None:
    try:
        data = bytes.fromhex(raw or "")
    except ValueError:
        return None
    width = profile.salt_weight_bytes
    if len(data) != width + 2:
        return None
    return int.from_bytes(data[:width], "little"), int.from_bytes(data[width:], "little")
