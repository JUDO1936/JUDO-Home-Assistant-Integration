# JUDO Home Assistant Integration

**Version 4.0.6 · Nutzergepflegte Home-Assistant-Integration für die i-soft-Familie**

**Maintainer dieser Weiterentwicklung:** Nutzer der Integration

> **Projektstatus:** Diese nutzergepflegte Weiterentwicklung wird von einem
> Nutzer betreut. Sie ist ein unabhängiges Community-Projekt und wird nicht im
> Auftrag des Geräteherstellers veröffentlicht, unterstützt oder als offizielles
> Produkt angeboten. Die Herstellerunterlagen dienen als technische Quelle für die REST-API.

Mit dieser Integration lassen sich unterstützte JUDO-i-soft-Anlagen über ihre
lokale REST-Schnittstelle in Home Assistant einbinden. Wasser- und Salzdaten
werden regelmäßig abgefragt. Je nach Modell können außerdem Einstellungen
geändert und Aktionen wie Regeneration, Szenen oder Leckageschutz ausgeführt werden.

Die REST-Kommandos sind anhand der technischen Dokumentation
`RESTAPI_Kommandos.pdf` umgesetzt. Das Dokument dient als technische Quelle;
es bedeutet keine offizielle Freigabe oder Unterstützung dieses Projekts.
Die Integration verwendet keine Cloud-Verbindung:
Home Assistant kommuniziert direkt mit der IP-Adresse der Anlage.

**Technischer Integrationsname:** `judo_home_assistant_integration`

## Inhalt

- [Unterstützte Geräte](#unterstützte-geräte)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Wechsel von der bisherigen PRO-Integration](#wechsel-von-der-bisherigen-pro-integration)
- [Einrichtung und mehrere Anlagen](#einrichtung-und-mehrere-anlagen)
- [Anzeigenamen und Entity-IDs](#anzeigenamen-und-entity-ids)
- [Sensoren und Bedienfunktionen](#sensoren-und-bedienfunktionen)
- [Bedienbeispiele](#bedienbeispiele)
- [Dashboard](#dashboard)
- [Automationsbeispiele](#automationsbeispiele)
- [Kommunikation und Aktualisierung](#kommunikation-und-aktualisierung)
- [Fehlerbehebung](#fehlerbehebung)
- [REST-Beispiele zur Diagnose](#rest-beispiele-zur-diagnose)
- [Grenzen dieser Version](#grenzen-dieser-version)
- [GitHub und Projektdateien](#github-und-projektdateien)
- [Prüfung und Versionshinweise](#prüfung-und-versionshinweise)

## Unterstützte Geräte

Der Gerätetyp wird beim Einrichten über `FF00` erkannt. Die Integration bietet
nur die für das jeweilige Modell vorgesehenen Entitäten an. Es gibt keine
manuelle Auswahl eines PRO-Profils für ein anderes Gerät.

| Modell | Gerätetyp, hex | Live-Status `69` | Szenen / PRO-Urlaub | Leckageaktion |
| --- | --- | --- | --- | --- |
| i-soft | `32`, `53` | nein | nein | Alarm setzen / zurücksetzen |
| i-soft K | `43`, `54` | nein | nein | Alarm setzen / zurücksetzen |
| i-soft SAFE+ | `33`, `57` | nein | nein | Schutz schließen / öffnen |
| i-soft K SAFE+ | `42`, `67` | nein | nein | Schutz schließen / öffnen |
| i-soft PRO | `58`, `4B` | ab SW: 2.5.48 | ja | Schutz schließen / öffnen |
| i-soft PRO L | `4C` | ab SW: 2.5.48 | ja | Schutz schließen / öffnen |
| i-soft PRO XL 70 | `6E` | ab SW: 2.5.48 | nein | Schutz schließen / öffnen |
| i-soft PRO XL 140 | `69` | ab SW: 2.5.48 | nein | Schutz schließen / öffnen |


Unbekannte Gerätetypen werden bei der Einrichtung abgelehnt. Andere Familien,
z. B. SOFTwell, ZEWA, i-dos oder i-fill, sind in dieser Version noch nicht enthalten,
diese werden aber Zeitnah folgen.

**Beispiel:** Ein i-soft K erhält Wasser-, Salz- und Härtewerte sowie
Alarmaktionen. Er erhält keine Szenenauswahl und keine PRO-Urlaubstage.
Ein PRO XL erhält Live-Daten, aber ebenfalls keine PRO-Szenenauswahl.

## Voraussetzungen

- Eine Anlage aus der oben aufgeführten Gerätefamilie.
- Eine erreichbare lokale REST-Schnittstelle an der Anlage.
- Home Assistant mit der Möglichkeit, benutzerdefinierte Integrationen zu installieren.
- IP-Adresse oder Hostname, REST-Port und Zugangsdaten der Anlage.
- Eine Netzwerkverbindung von Home Assistant zur Anlage. Bei getrennten
  Netzwerksegmenten muss der konfigurierte Port zwischen beiden erreichbar sein.

Alle Geräte außer die von der i-soft PRO Familie benötigten ein Connectivity Modul. 
Nur mit diesem sind die Geräte überhaupt erst Internet fähig.

Der Client verwendet HTTP und HTTP-Basic-Authentifizierung. Eine Einrichtung
mit HTTPS, Zertifikaten oder einem frei wählbaren URL-Pfad ist nicht enthalten.
Im Feld „IP-Adresse / Hostname“ nur die Adresse eintragen, z. B. `192.168.1.50`:
kein `http://`, kein `/api/rest` und keinen Port an die Adresse anhängen.

Der Port wird im eigenen Eingabefeld angegeben. Standard ist `80`.
Eine feste IP-Adresse oder eine DHCP-Reservierung hilft, die Anlage auch nach
Neustarts unter derselben Adresse zu erreichen.

## Installation

### Manuell installieren

1. ZIP-Datei entpacken.
2. Den vollständigen Ordner `custom_components/judo_home_assistant_integration`
   nach `/config/custom_components/` kopieren.
3. Prüfen, dass die Datei danach hier liegt:
   `/config/custom_components/judo_home_assistant_integration/manifest.json`.
4. Home Assistant vollständig neu starten. Ein reines Neuladen des Dashboards
   lädt die Python-Dateien der Integration nicht neu.
5. Unter **Einstellungen → Geräte & Dienste** eine Integration hinzufügen
   und **JUDO Home Assistant Integration** auswählen.
6. Die Anlage wie im Abschnitt „Einrichtung“ beschrieben hinzufügen.

Kopiere den Integrationsordner nicht zusätzlich in einen zweiten Projektordner
unter `custom_components`. Entscheidend ist der oben genannte direkte Pfad
zur `manifest.json`.

### Bereits installierte Version 4.x aktualisieren

1. Home-Assistant-Konfiguration und bisherigen Integrationsordner sichern.
2. Den vollständigen neuen Integrationsordner einsetzen und vorhandene Dateien
   ersetzen. Dateien verschiedener Versionen nicht mischen.
3. Home Assistant vollständig neu starten.
4. Die Geräte und Entitäten kontrollieren.

Ein Update innerhalb derselben Domain erfordert grundsätzlich keinen Wechsel
zur alten PRO-Domain. Versionsspezifische Hinweise in der jeweiligen Veröffentlichung
gehen dieser allgemeinen Anleitung vor.

### Installation über HACS

Wenn das Repository unter dem unten angegebenen Namen veröffentlicht wurde,
kann es in HACS als benutzerdefiniertes Repository des Typs **Integration**
hinzugefügt und installiert werden. Danach ist ebenfalls ein vollständiger
Neustart von Home Assistant erforderlich.

Diese ZIP-Datei allein veröffentlicht das Repository nicht. Falls der neue
Repository-Name auf GitHub noch nicht existiert, verwende zunächst die manuelle
Installation. Prüfe bei einem Wechsel, dass HACS nicht weiterhin die alte
PRO-Version als Quelle für dieselbe Anlage verwaltet.

#
## Einrichtung und mehrere Anlagen

### Beispiel für eine Anlage

| Eingabefeld | Beispiel | Bedeutung |
| --- | --- | --- |
| Gerätename | `i-soft Keller` | Frei wählbarer Anzeigename |
| IP-Adresse / Hostname | `192.168.1.50` | Lokale Adresse der Anlage |
| Port | `80` | Port der REST-Schnittstelle |
| Benutzername | `admin` | Standardvorgabe; bei Änderung anpassen |
| Passwort | `Connectivity` | Standardvorgabe; bei Änderung anpassen |

Die Standardvorgaben sind keine Garantie für die Zugangsdaten jeder Anlage.
Verwende die tatsächlich am Gerät gültigen Daten.

Nach dem Absenden liest die Integration zuerst den Gerätetyp und anschließend
die Gerätenummer. Die Gerätenummer dient zur Erkennung einer bereits
innerhalb dieser Integration eingerichteten Anlage.

Der Gerätename kann über den angebotenen Schritt zum Neukonfigurieren geändert
werden. Dieser Schritt ändert in der aktuellen Version nur den Namen, nicht
IP-Adresse, Port oder Zugangsdaten.

### Beispiel mit zwei Anlagen

| Anlage | Gerätename | IP-Adresse | Eigener Eintrag |
| --- | --- | --- | --- |
| i-soft K SAFE+ | `i-soft Keller` | `192.168.1.50` | ja |
| i-soft PRO | `i-soft Werkstatt` | `192.168.1.51` | ja |

Die Integration einmal installieren und anschließend für jede Anlage einen
eigenen Konfigurationseintrag hinzufügen. Die Geräte müssen nicht dieselben
Funktionen haben. Home Assistant erhält für jedes Gerät dessen eigenes Profil.

## Anzeigenamen und Entity-IDs

Ein Anzeigename und eine Entity-ID erfüllen unterschiedliche Aufgaben.

- Der **Anzeigename** orientiert sich am Namen bei der Einrichtung und der
  Funktion, z. B. „i-soft Keller Salzgewicht“.
- Die **Entity-ID** ist die technische Referenz für Dashboards und Automationen.
  Neue Entitäten verwenden die Domain plus die konfigurierte Geräteadresse.
- Das **Modell** wird aus der API erkannt und ist unabhängig vom frei
  gewählten Gerätenamen.

Für `192.168.1.50` am Standardport entstehen beispielsweise diese Vorgaben:

| Funktion | Beispiel-Entity-ID |
| --- | --- |
| Salzgewicht | `sensor.judo_home_assistant_integration_192_168_1_50_salzgewicht` |
| Salzreichweite | `sensor.judo_home_assistant_integration_192_168_1_50_salzreichweite` |
| Gerätestatus | `sensor.judo_home_assistant_integration_192_168_1_50_geratestatus` |
| Härte einstellen | `number.judo_home_assistant_integration_192_168_1_50_wunschwasserharte` |
| Regeneration | `button.judo_home_assistant_integration_192_168_1_50_regeneration_starten` |

Bei Port `8080` lautet der Präfix beispielsweise:
`judo_home_assistant_integration_192_168_1_50_p8080`.
Bei Hostnamen werden für die Vorgabe Buchstaben kleingeschrieben und
Sonderzeichen durch Unterstriche ersetzt.

Die genannten IDs sind **Vorgaben für neue Entitäten**. Manuell geänderte IDs
oder Konflikte in der Entity-Registry können zu anderen IDs führen. Übernimm
deshalb für YAML immer die tatsächlich im Gerätebildschirm angezeigte ID.
Eine Änderung des Anzeigenamens benennt vorhandene Entity-IDs nicht automatisch um.

## Sensoren und Bedienfunktionen

### Basiswerte für alle unterstützten Modelle

| Sensor | Einheit / Darstellung | Erläuterung |
| --- | --- | --- |
| Gesamtwassermenge | m³ | Vom Gerät gemeldeter kumulierter Zähler |
| Weichwassermenge | m³ | Vom Gerät gemeldeter kumulierter Weichwasserzähler |
| Salzgewicht | kg | Gerätewert für den Salzvorrat |
| Salzreichweite | Tage | Gerätewert für die voraussichtliche Reichweite |
| Wunschwasserhärte | Eingestellte Härteeinheit | Gewählter Sollwert; keine separate Rohwasserhärtemessung |
| Software-Version | Versionsangabe | Steuerungssoftware des Geräts |
| Gerätetyp | Modellname | Aus dem Gerätetypcode erkannt |
| Gerätestatus | Online / Offline | Aus dem Zeitpunkt der letzten erfolgreichen Antwort abgeleitet |

Beispiel: Ein Gerätewert von `1057516` Litern wird als `1057,516 m³`
dargestellt. Ein Salzgewicht von `21750` Gramm erscheint als `21,75 kg`.
Die Anzeige entspricht den gemeldeten Gerätewerten; sie ist keine zusätzliche
Gewichts- oder Verbrauchsmessung durch Home Assistant.

Die Software-Version wird beim Start und anschließend einmal pro Stunde
abgefragt. Die Salzmangel-Warnschwelle wird als Zahl in Tagen angezeigt. Bei
der maximalen Entnahmedauer zeigt die Auswahl auch einen aktuell eingestellten
Wert an, selbst wenn dieser nicht zu den üblichen Auswahlstufen gehört.

### Gemeinsame Einstellungen und Aktionen

| Bedienpunkt | Bereich / Funktion |
| --- | --- |
| Wunschwasserhärte | 0–30 °dH, Schrittweite 1; zum Einstellen zuerst °dH wählen |
| Härteeinheit | Modellabhängige Auswahl |
| Salzmangel-Warnschwelle | 0–30 Tage; Einstellung wird an die Anlage übertragen |
| Regeneration starten | Sendet den dokumentierten Startbefehl |
| Leckageaktion | Je nach Modell Alarm oder Absperrschutz |

Die Integration bietet bei Standardmodellen °dH,°fH, ppm, mmol 

Die Warnschwelle in Tagen ist eine Geräteeinstellung. Eine zusätzliche
Home-Assistant-Meldung wird dadurch nicht automatisch eingerichtet; dafür kann
eine eigene Automation erstellt werden.

### PRO / PRO L zusätzlich

- Szenenauswahl und Sofortaktivierung.
- Szenendauer: 15, 30, 45 Minuten; 1, 2, 6, 12 Stunden; unbegrenzt.
- Urlaubstage zwischen 1 und 60 und separater Start des Urlaubsmodus.
- Maximale Entnahmemenge: 0–3000 L, angebotene Schritte 100 L.
- Maximaler Volumenstrom: 0–5000 L/h, angebotene Schritte 250 L/h.
- Maximale Entnahmedauer: deaktiviert oder angebotene Zeiten bis 255 Minuten.
- Live-Durchfluss, Wassertemperatur, aktive Szene und Leckageinformationen.

Bei den PRO-Grenzwerten bedeutet `0` laut API-Dokumentation deaktivierte
Überwachung. Die Integration bietet keine beliebigen Zeiten über 255 Minuten
an, weil Kommando `3E` einen Ein-Byte-Wert verwendet.

### PRO XL zusätzlich

PRO XL erhält Live-Durchfluss, Wassertemperatur und Leckageinformationen,
aber keine PRO-Szenen, Urlaubstage oder PRO-Grenzwertregler.

Die Salzantwort hat ein größeres Format: **4 Bytes Gewicht + 2 Bytes
Reichweite**. Bei den übrigen Modellen werden **2 + 2 Bytes** ausgewertet.
Zusätzliche Bytes hinter den dokumentierten Werten werden ignoriert.

### Leckagealarm und Leckageschutz unterscheiden

| Gerätefamilie | Bedeutung der Aktionen |
| --- | --- |
| i-soft / i-soft K | „Leckagealarm setzen“ und „Leckagealarm zurücksetzen“ |
| SAFE+ / K SAFE+ / PRO / PRO L / PRO XL | „Leckageschutz schließen“ und „Leckageschutz öffnen“ |

Bei i-soft/i-soft K darf aus dem Alarmbefehl nicht auf ein geschlossenes
Absperrventil geschlossen werden. Die technischen Button-Suffixe
`leckageschutz_offnen` und `leckageschutz_schliessen` werden auch bei den
Alarmmodellen verwendet; ihre Anzeigenamen beschreiben die richtige Funktion.

„Leckageschutz Position (abgeleitet)“ ist keine separat gemessene Ventilstellung.
Die Integration zeigt bei Leckagegrund `00` „Geöffnet“ und bei gesetzten
Leckagegrund-Bits „Geschlossen“. Für die Bewertung bleibt der tatsächliche
Gerätezustand maßgeblich.

## Bedienbeispiele

### Wunschwasserhärte auf 7 °dH einstellen

1. Die Entität „Härteeinheit“ auf **°dH** setzen.
2. Die Rückmeldung abwarten; die Integration liest die Einheit nach.
3. „Wunschwasserhärte“ auf **7** setzen.
4. Nach der Rücklesung den Härtesensor kontrollieren.

Die Integration sendet die Härte als dokumentierten Ein-Byte-Wert in °dH.
Bei einer anderen Geräte-Einheit ist der Härteregler nicht verfügbar.
Der Härtesensor zeigt weiterhin den Gerätewert in der ausgewählten Einheit.

### Regeneration starten

Im Gerätebildschirm oder Dashboard den Button **„Regeneration starten“**
drücken. Der Befehl wird an die Anlage gesendet. Einen eigenen Sensor, der
Start, Fortschritt und Abschluss der Regeneration bestätigt, enthält diese
Version nicht. Eine erfolgreiche REST-Anfrage ist daher keine Bestätigung,
dass die vollständige Regeneration bereits beendet wurde.

### PRO-Szene „Garten bewässern“ für zwei Stunden

1. In „Szenenauswahl“ **Garten bewässern** auswählen.
2. In „Szenendauer“ **02:00** auswählen.
3. **Szene aktivieren** drücken.
4. Die Rückmeldung „Aktive Szene“ nach der Statusabfrage kontrollieren.

Die Auswahl allein sendet noch keinen Szenenstart: Erst der Button aktiviert
sie. **Alltag meistern** ist nicht Teil der Auswahlliste. Verwende dafür den
eigenen Button, der die Anlage auf die unbegrenzte Grundszene zurückstellt.
„Urlaub genießen“ wird separat über Urlaubstage und den Urlaubsmodus-Button
bedient.

### PRO-Urlaub für fünf Tage

1. „Urlaubstage“ auf **5** setzen.
2. **Urlaubsmodus starten** drücken.
3. Die Rückmeldung der Anlage kontrollieren.

Die Urlaubstage sind zunächst ein lokal gespeicherter Bedienwert. Erst der
Start-Button überträgt den Urlaub an die Anlage. Ein eigener Button zum
Beenden des Urlaubs ist in dieser Version nicht enthalten.

### Leckageaktion verwenden

Bei einem SAFE+- oder PRO-Gerät bewirken die Buttons die dokumentierten
Öffnungs-/Schließbefehle. Bei einem klassischen i-soft wird der Alarm gesetzt
oder zurückgesetzt. Verwende die Aktionen entsprechend der angezeigten
Gerätefunktion; ein Alarm ist nicht gleichbedeutend mit einer Absperrung.

## Dashboard

Die Integration erstellt Entitäten, aber kein automatisch angepasstes Dashboard.
Die YAML-Vorlagen müssen passend zum Modell und den tatsächlichen IDs gewählt werden.

| Datei | Geeignet für | Inhalt |
| --- | --- | --- |
| `dashboard.yaml` | Alle unterstützten Modelle | Basiswerte, gemeinsame Einstellungen und Aktionen |
| `dashboard-pro.yaml` | PRO / PRO L | Beispiel-Dashboard mit Live-Daten, Szenen und Urlaub; Beispiel-IDs müssen angepasst werden |

Die Basisvorlage kann auch für PRO und PRO XL verwendet werden. Für XL können
Live-Karten ergänzt werden, aber nicht die Szenen-/Urlaubskarten der PRO-Vorlage.
Die Szenenvorlage bei einem klassischen i-soft zu verwenden würde fehlende
Entitäten anzeigen.

### Dashboard-Vorlage für die eigene Anlage anpassen

Die YAML-Dateien sind Beispiele. Home Assistant ersetzt die Beispiel-IDs nicht
automatisch und der frei gewählte Gerätename wird nicht zwingend Teil der
Entity-ID. Neue Vorgabe-IDs verwenden die Geräteadresse und bei abweichendem
Port zusätzlich `_pPORT`; vorhandene oder manuell geänderte IDs können anders
lauten.

1. In Home Assistant **Einstellungen → Geräte & Dienste** öffnen.
2. **JUDO Home Assistant Integration** und anschließend das gewünschte Gerät
   auswählen.
3. Unter **Entitäten** die vollständigen Entity-IDs der benötigten Werte und
   Bedienelemente kopieren. Der Anzeigename wie „Salzgewicht“ ist nicht die
   Entity-ID.
4. Die passende Datei `dashboard.yaml` oder `dashboard-pro.yaml` öffnen.
   Die Beispiel-IDs beginnen mit
   `judo_home_assistant_integration_192_168_1_50`. Ersetze diesen Präfix durch
   den Präfix deiner Anlage. Falls einzelne Entity-IDs abweichen oder manuell
   umbenannt wurden, ersetze diese vollständigen IDs einzeln.
5. Ändere Dashboard-Titel und `path`, damit du deine Anlage wiedererkennst,
   zum Beispiel `i-soft PRO PP1` und `judo-pro-pp1`.
6. Übernimm die vollständige YAML-Datei in ein YAML-Dashboard. Bei einem schon
   vorhandenen Dashboard fügst du nur den Inhalt unter `views:` als Ansicht ein;
   ersetze nicht ungeprüft die gesamte Konfiguration.
7. Speichern und prüfen, ob keine Karte „Entität nicht gefunden“ meldet.

Für jede weitere Anlage kopierst du die Vorlage erneut und setzt die Entity-IDs
dieser Anlage ein. So bleiben die Anlagen und ihre Werte eindeutig zugeordnet.

Eine Datei mit `views:` ist keine einzelne Kartenkonfiguration. Für den
Karteneditor stattdessen nur den jeweiligen Kartenblock ab `type:` verwenden.

### Beispiel: einzelne Salzkarte

```yaml
type: entities
title: i-soft Keller – Salzvorrat
show_header_toggle: false
entities:
  - entity: sensor.judo_home_assistant_integration_192_168_1_50_salzgewicht
    name: Salzgewicht
  - entity: sensor.judo_home_assistant_integration_192_168_1_50_salzreichweite
    name: Reichweite
  - entity: number.judo_home_assistant_integration_192_168_1_50_salzmangel_warnschwelle
    name: Warnschwelle in Tagen
```

### Beispiel: Regeneration als Button-Karte

```yaml
type: button
name: Regeneration starten
icon: mdi:refresh
entity: button.judo_home_assistant_integration_192_168_1_50_regeneration_starten
tap_action:
  action: perform-action
  perform_action: button.press
  target:
    entity_id: button.judo_home_assistant_integration_192_168_1_50_regeneration_starten
```

Für eine zweite Anlage alle Referenzen dieser Karte auf deren eigenen Präfix
ändern. Beide Anlagen dürfen unterschiedliche Dashboard-Vorlagen verwenden.

## Automationsbeispiele

Die folgenden Beispiele verwenden die Beispiel-IP `192.168.1.50`.
Ersetze alle Entity-IDs vor Verwendung. Die Beispiele erzeugen Meldungen
innerhalb von Home Assistant, versenden aber keine E-Mails oder Nachrichten.

### Meldung bei weniger als fünf Tagen Salzreichweite

```yaml
alias: JUDO – Salzreichweite unter 5 Tagen
triggers:
  - trigger: numeric_state
    entity_id: sensor.judo_home_assistant_integration_192_168_1_50_salzreichweite
    below: 5
actions:
  - action: persistent_notification.create
    data:
      title: JUDO – Salz nachfüllen
      message: Die gemeldete Salzreichweite ist unter fünf Tage gefallen.
mode: single
```

Die Automation reagiert auf das Unterschreiten der Grenze. Sie erzeugt keine
regelmäßige tägliche Erinnerung, solange der Wert darunter bleibt. Ist der
Sensor „unbekannt“, liegt kein auswertbarer numerischer Wert vor.

### Meldung, wenn die Anlage fünf Minuten „Offline“ meldet

```yaml
alias: JUDO – Anlage offline
triggers:
  - trigger: state
    entity_id: sensor.judo_home_assistant_integration_192_168_1_50_geratestatus
    to: "Offline"
    for: "00:05:00"
actions:
  - action: persistent_notification.create
    data:
      title: JUDO – Verbindung prüfen
      message: Die Anlage meldet seit fünf Minuten Offline.
mode: single
```

Der Gerätestatus selbst hat bereits eine Schwelle von fünf Minuten seit der
letzten erfolgreichen Antwort. Die Automation wartet zusätzlich fünf Minuten
im Zustand „Offline“. Sie reagiert nicht auf den separaten HA-Zustand
`unavailable`. Die Zustandsmeldung ist außerdem an veröffentlichte Updates
gebunden und kein sekundengenauer Netzwerktest.

### Beispiel für einen manuellen Aktionsaufruf

Für einen manuellen Aufruf der Regeneration kann dieser Aktionsblock verwendet
werden, etwa in einem Skript oder im YAML-Modus des Aktionswerkzeugs:

```yaml
action: button.press
target:
  entity_id: button.judo_home_assistant_integration_192_168_1_50_regeneration_starten
```

Der Block löst die Aktion tatsächlich aus. Für eine reine Verbindungsdiagnose
stattdessen die unten aufgeführten Leseabfragen verwenden.

## Kommunikation und Aktualisierung

| Vorgang | Verhalten dieser Version |
| --- | --- |
| Basiswerte | Abfrageintervall 2 Minuten |
| PRO-/XL-Live-Status | Zusätzlich alle 100 Sekunden |
| Abstand zwischen Anfragen | Mindestens 1 Sekunde je Geräteclient |
| Reihenfolge | Serialisiert über eine gemeinsame Anfragewarteschlange |
| Rücklesen nach vielen Einstellungen | Nach etwa 5 Sekunden eingeplant, gegebenenfalls später durch die Warteschlange |
| Request-Timeout | 10 Sekunden |
| Wiederholung von Leseanfragen | Bei bestimmten Transport-/Serverfehlern einmal |
| Wiederholung von Schreibanfragen | Keine automatische Wiederholung nach einem Fehler |
| Online-Bewertung | Erfolgreiche Antwort innerhalb der letzten 5 Minuten |

Nicht alle Werte aktualisieren sich gleichzeitig. Bei mehreren Kommandos
benötigt ein vollständiger Durchlauf einige Sekunden; Timeouts und Warteschlange
können ihn verlängern. Die Intervalle sind in dieser Version nicht über ein
Optionsmenü einstellbar.

Bei Fehlern bleiben zuletzt gültige Werte im Cache erhalten. Sichtbare Werte
können deshalb älter als der letzte Aktualisierungsversuch sein. Einige
Sensoren können bei einem fehlgeschlagenen Coordinator-Update zusätzlich als
nicht verfügbar erscheinen. „Online“ bedeutet, dass mindestens eine Abfrage
kürzlich erfolgreich war; es bestätigt nicht, dass jedes Kommando funktioniert.

Schreibbefehle werden nach einem Timeout nicht automatisch wiederholt, weil die
Anlage die Aktion möglicherweise bereits ausgeführt hat. Prüfe vor einem
manuellen erneuten Start zunächst den Zustand der Anlage.

## Fehlerbehebung

### Integration wird nicht angeboten

- Prüfen, dass die `manifest.json` direkt im neuen Integrationsordner liegt.
- Prüfen, dass Ordnername und Domain `judo_home_assistant_integration` lauten.
- Den vollständigen Ordner verwenden, nicht nur `manifest.json` oder einzelne
  Python-Dateien aus verschiedenen Versionen.
- Home Assistant vollständig neu starten und die Protokolle kontrollieren.

### Einrichtung meldet einen Verbindungsfehler

- IP-Adresse und Port prüfen; keine vollständige URL ins Hostfeld eintragen.
- Benutzername und Passwort der Anlage prüfen.
- Netzwerkzugriff von Home Assistant zur Anlage kontrollieren.
- Eine lesende REST-Abfrage testen, siehe nächster Abschnitt.

Eine funktionierende Browserabfrage vom eigenen PC belegt noch nicht, dass
Home Assistant aus seinem Netzwerksegment dieselbe Anlage erreichen kann.

### Gerät wird als nicht unterstützt gemeldet

Den tatsächlichen Gerätetyp aus `FF00` mit der Tabelle vergleichen.
Ein unbekannter Code wird nicht durch einen beliebigen Modellnamen beim
Einrichten unterstützt. Für die Ergänzung eines neuen Typs werden dessen
Gerätekennung und eine passende API-Beschreibung benötigt.

### Salzgewicht und Reichweite zeigen „unbekannt“

Beide Werte kommen aus **derselben Antwort auf `5600`**. Deshalb prüfen:

1. Ist die aktuelle Salzkorrektur installiert? Sie ist ab Version 3.0.2 und
   auch in Version 4.0.0 enthalten.
2. Wurde Home Assistant nach dem Austausch vollständig neu gestartet?
3. Ist die Salzantwort vorhanden und als Hex-Daten auswertbar?
4. Passt die benötigte Mindestlänge zum erkannten Modell?

Frühere Familienversionen verlangten eine exakt passende Antwortlänge.
Die ursprüngliche Integration akzeptierte zusätzliche Bytes. Dieses Verhalten
ist wiederhergestellt: Standardmodelle benötigen mindestens 4 Bytes, XL
mindestens 6 Bytes; weitere Bytes werden ignoriert.

Die Korrektur behebt nicht jede denkbare Ursache. Eine leere, zu kurze,
fehlerhafte oder fehlende API-Antwort liefert weiterhin keinen Sensorwert.
Für eine Untersuchung Gerätetyp, Version, vollständige Antwort auf `5600`
und relevante Protokollzeilen angeben. Zugangsdaten nicht mitsenden.

### Nur Live-Werte fehlen

Bei klassischen und SAFE+-Geräten sind die PRO-Live-Entitäten nicht vorgesehen.
Bei PRO/XL die Firmware und die Antwort auf `6900` prüfen. Funktionierende
Salz-/Wasserwerte bestätigen nicht automatisch die Unterstützung von `69`.

### Dashboard zeigt „Entität nicht gefunden“

- Eine Vorlage für die richtige Gerätefamilie verwenden.
- Tatsächliche IDs aus Home Assistant übernehmen.
- Nach dem Domain-Wechsel alte `judo_isoft_pro`-Referenzen ersetzen.
- Beispiel-IP und gegebenenfalls `_pPORT` anpassen.

„Entität nicht gefunden“ bezeichnet eine falsche oder fehlende Referenz.
„Unbekannt“ bezeichnet eine vorhandene Entität ohne auswertbaren Wert.
„Nicht verfügbar“ ist ein eigener Zustand; diese Meldungen nicht gleichsetzen.

### Szenenstart funktioniert nicht

- Prüfen, dass ein PRO oder PRO L eingerichtet ist.
- In „Szenenauswahl“ zuerst eine auswählbare Szene wählen; „Alltag meistern“
  und „Urlaub genießen“ werden dort nicht angeboten.
- Danach die Dauer einstellen und zusätzlich „Szene aktivieren“ drücken.
- Für die Rückkehr zur Grundszene den eigenen Button „Alltag meistern“ verwenden.
- Urlaub über die separaten Urlaubstage und den Urlaubsstart bedienen.
- Relevante Protokollmeldung und Statusrückmeldung prüfen.

### Härteregler ist nicht verfügbar

Zuerst die Härteeinheit auf °dH setzen und die Rücklesung abwarten.
Die Reglerfreigabe hängt vom zurückgelesenen Einheitenwert ab, nicht allein
von der zuletzt im Dashboard angeklickten Auswahl.

### Alte und neue Geräte erscheinen doppelt

Kontrollieren, ob die Anlage noch unter beiden Domains eingerichtet ist.
Vor dem Entfernen alter Einträge Referenzen sichern und umstellen. Die
Erkennung der Gerätenummer verhindert keine Doppeleinrichtung über zwei
verschiedene Integrationen hinweg.

## REST-Beispiele zur Diagnose

Die folgenden URLs sind **Leseabfragen**. `192.168.1.50` durch die Geräteadresse
ersetzen. Wenn der Browser eine Anmeldung verlangt, die Geräte-Zugangsdaten
verwenden. Bei abweichendem Port lautet der Anfang beispielsweise
`http://192.168.1.50:8080/api/rest/`.

| Information | Beispiel-URL |
| --- | --- |
| Gerätetyp | `http://192.168.1.50/api/rest/FF00` |
| Gerätenummer | `http://192.168.1.50/api/rest/0600` |
| Salzgewicht und Reichweite | `http://192.168.1.50/api/rest/5600` |
| Härteeinheit | `http://192.168.1.50/api/rest/2300` |
| Wunschwasserhärte | `http://192.168.1.50/api/rest/5100` |
| PRO-/XL-Live-Status | `http://192.168.1.50/api/rest/6900` |

Die vollständige JSON-Hülle kann je nach Gerät abweichen. Entscheidend ist
das vom Client ausgelesene Feld `data`.

### Beispiel einer Standard-Salzantwort

```json
{"data":"F6541100"}
```

- `F654`: Little-Endian-Wert `0x54F6` = 21750 Gramm = **21,75 kg**.
- `1100`: Little-Endian-Wert `0x0011` = **17 Tage**.

### Beispiel einer XL-Salzantwort

```json
{"data":"F7A302001700"}
```

- `F7A30200`: Little-Endian-Wert `0x0002A3F7` = 173047 Gramm,
  auf zwei Nachkommastellen dargestellt als **173,05 kg**.
- `1700`: Little-Endian-Wert `0x0017` = **23 Tage**.

Es wird anhand des erkannten Modells entschieden, ob das Gewicht zwei oder
vier Bytes umfasst. Die Antwort wird nicht allein anhand ihrer Länge als
anderes Gerätemodell interpretiert.

## Grenzen dieser Version

- SAFE+-Urlaub verwendet ein anderes Bitfeld als PRO. Eine zuverlässige
  Rücklesung der vorhandenen Optionen ist in der verwendeten Unterlage nicht
  belegt; der Modus wird daher hier nicht angeboten. Bedienung am Gerät bleibt möglich.
- Bei klassischen und SAFE+-Geräten sind die Beschreibungen von `3F` und `40`
  bezüglich Bezeichnung/Einheit uneindeutig; außerdem fehlt dort eine belegte
  Rücklesefunktion. Diese Grenzwertregler werden nicht angeboten.
- PRO XL hat keine in diesem Profil belegten PRO-Grenzwertkommandos.
- Historische Tages-, Wochen-, Monats- und Jahresstatistiken über `FB`–`FE`
  sind noch nicht als eigene Entitäten eingebaut. HA-Verläufe basieren auf den
  ab Einrichtung erfassten Sensorwerten und importieren keine Gerätehistorie.
- Serviceadresse, Salzvorrat-Schreiben und Szenenbearbeitung sind keine eigenen
  Bedienpunkte dieser Version. Der Button „Alltag meistern“ stellt die
  Grundszene wieder her.
- Automatische Dashboard-Anpassung und automatische Migration der alten Domain
  sind nicht enthalten.
- Homeguard-Meldungen können bei unterstütztem Live-Status als Leckagegrund
  erscheinen. Eine eigene Verwaltung einzelner Homeguard-Geräte ist nicht eingebaut.
- Es wurde keine Mindestversion von Home Assistant durch einen Installationstest
  bestätigt. Für die verwendeten Entitäts- und Dashboard-Funktionen muss die
  jeweilige HA-Version kompatibel sein.

## Projektseite und Projektdateien

Diese Anleitung und die Weiterentwicklung werden von einem Nutzer gepflegt. Die
Dokumentationsadresse in `manifest.json` verweist auf das ursprüngliche
Upstream-Projekt und dient nur als technische Referenz. GitHub-Zuordnungen für
Codeverantwortung und Issues sind entfernt, damit Anfragen nicht an das
Upstream-Projekt geleitet werden. Sobald eine persönliche Repository-Adresse
veröffentlicht ist, kann sie hier als Projekt- und Kontaktadresse eingetragen werden.

Den **Inhalt des entpackten Projektordners** hochladen, sodass `README.md`,
`hacs.json` und `custom_components` direkt im Repository-Stamm liegen.
Der Integrationsordner selbst heißt `judo_home_assistant_integration`.

| Datei / Ordner | Zweck | Bei manueller HA-Installation benötigt? |
| --- | --- | --- |
| `custom_components/judo_home_assistant_integration/` | Vollständige Integration | ja, gesamter Ordner |
| `manifest.json` innerhalb der Integration | Domain, Anzeigename, Version, GitHub-Links | ja |
| `models.py` | Gerätetypen und Fähigkeiten; Salzformat | ja |
| `api.py` | REST-Zugriff und Anfragewarteschlange | ja |
| `coordinator.py` | Abfrage, Cache und Rücklesen | ja |
| `config_flow.py` | Einrichtung und Gerätename | ja |
| `const.py`, `protocol.py`, `__init__.py` | Gemeinsame Definitionen, Statusdecodierung und Einrichtung | ja |
| `sensor.py`, `number.py`, `select.py`, `button.py` | Home-Assistant-Entitäten | ja |
| `strings.json`, `translations/`, `brand/` | Texte, Übersetzungen und Grafiken | als Teil des vollständigen Ordners mitkopieren |
| `dashboard.yaml` | Basis-Dashboard | optional, YAML übernehmen |
| `dashboard-pro.yaml` | PRO-/PRO-L-Dashboard | optional, Beispiel-IDs vor dem Import ersetzen |
| `www/judo_home_assistant_integration/` | Zusätzliche Grafikdateien | optional; die beiliegenden Dashboard-Vorlagen referenzieren sie nicht |
| `hacs.json` | Repository-Metadaten für HACS | im Repository, nicht separat in den HA-Integrationsordner |
| `tests/` | Simulierte Entwicklungstests | nein |
| `README.md`, `LICENSE.md` | Dokumentation und Lizenz | nicht für den HA-Laufzeitbetrieb |
| `example_automation` | Beispiel Automation für eine Meldung bei Geschlossenen Leckageschutz |

Der allgemeine Name „JUDO Home Assistant Integration“ bedeutet nicht, dass alle
JUDO-Produkte unterstützt werden. Maßgeblich bleibt die Gerätetabelle dieser Version.

## Prüfung und Versionshinweise

Die Version wurde mit **26 automatisierten Tests mit simulierten Antworten**
geprüft. Dabei werden unter anderem kontrolliert:

- Die 13 dokumentierten Gerätetypcodes und die Zuordnung zu Geräteprofilen.
- Ablehnung unbekannter Typen.
- Salzformate für Standard- und XL-Geräte einschließlich zusätzlicher Bytes.
- Decodierung der Live-Statuswerte.
- Auswahl der passenden Plattform-Entitäten je Familie.
- Payloads für Härte, Szenen und Urlaub.
- Keine automatische Wiederholung von Schreibanfragen nach Timeout.
- Cache-Verhalten bei fehlerhaften Antworten.
- Neue Domain und Entity-Präfixe.

Die Referenzen beider Dashboard-Vorlagen wurden zusätzlich gegen die erzeugten
PRO-Entitäten geprüft. Die Tests verwenden kleine Home-Assistant-Schnittstellen-
attrappen. **Sie ersetzen keinen Test mit einer laufenden Home-Assistant-Instanz
und echter Anlage.** Insbesondere Firmwareverhalten und tatsächliche Aktionsausführung
müssen am Gerät bestätigt werden.

Tests im Projektverzeichnis starten; die Python-Umgebung benötigt `aiohttp`:

```bash
python3 -m unittest discover -s tests -v
```

