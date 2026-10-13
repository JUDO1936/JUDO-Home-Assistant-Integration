# JUDO Home Assistant Integration

Version 3.0.1 · Lokale Integration für die i-soft-Familie

Erweiterung der bereitgestellten PRO-Integration anhand der mitgelieferten
RESTAPI_Kommandos.pdf. Lokale REST-Verbindung, ohne Cloud.
Der Domain-/Ordnername `judo_isoft_pro` bleibt aus Kompatibilitätsgründen erhalten.

## Unterstützte Geräte

| Modell | Gerätetyp (hex) | Live-Status 69 | Szenen / PRO-Urlaub | Leckageaktion |
| --- | --- | --- | --- | --- |
| i-soft | 32, 53 | nein | nein | Alarm setzen / zurücksetzen |
| i-soft K | 43, 54 | nein | nein | Alarm setzen / zurücksetzen |
| i-soft SAFE+ | 33, 57 | nein | nein | Schutz schließen / öffnen |
| i-soft K SAFE+ | 42, 67 | nein | nein | Schutz schließen / öffnen |
| i-soft PRO | 58, 4B | ja* | ja | Schutz schließen / öffnen |
| i-soft PRO L | 4C | ja* | ja | Schutz schließen / öffnen |
| i-soft PRO XL 70 | 6E | ja* | nein | Schutz schließen / öffnen |
| i-soft PRO XL 140 | 69 | ja* | nein | Schutz schließen / öffnen |

Bei älterer Firmware kann es sein das, dass Kommando 69 und Sensoren nicht verfügbar;
die Basiswerte funktionieren unabhängig davon. Unbekannte Gerätetypen werden abgelehnt.
Andere Produktfamilien wie SOFTwell, ZEWA oder i-dos sind nicht enthalten.

## Installation / bestehende Integration aktualisieren

1. Sichere den bisherigen Ordner `/config/custom_components/judo_isoft_pro`.
2. Kopiere den **gesamten Ordner** `custom_components/judo_isoft_pro` aus diesem
   ZIP nach `/config/custom_components/` und ersetze den bisherigen Inhalt.
   Alle enthaltenen Python- und JSON-Dateien gehören zusammen, einschließlich
   der neuen `models.py`. Keine einzelne Datei separat aktualisieren.
3. Starte Home Assistant vollständig neu.
4. Ein bestehender PRO-Eintrag kann weiterverwendet werden. Domain, Entry-Version
   und Unique-IDs der bisherigen Entitäten bleiben erhalten.
5. Weitere Geräte unter Einstellungen → Geräte & Dienste → Integration
   hinzufügen → **JUDO Home Assistant Integration** hinzufügen. Namen, IP-Adresse, Port und
   Zugangsdaten eintragen. Standard: Port 80, Benutzer `admin`, Passwort
   `Connectivity`; geänderte Zugangsdaten entsprechend eintragen.

Jedes Gerät erhält einen eigenen Eintrag. Der Typ wird über `FF00` erkannt,
die Gerätenummer über `0600` dient zur Vermeidung doppelter Einrichtung.
Bei einer HACS-Verwaltung können spätere Updates des ursprünglichen Repositories
diese manuell installierte Erweiterung überschreiben. Das ZIP veröffentlicht
keine Änderung am ursprünglichen Repository.

## Funktionen

Alle Modelle: Gesamt-/Weichwassermenge in m³, Salzgewicht in kg,
Salzreichweite, Wunschwasserhärte, Härteeinheit, Softwareversion,
Gerätetyp/-nummer, Betriebsstunden und Verbindungsstatus.
Aktionen: Regeneration, Härte einstellen, Härteeinheit wählen,
Salzmangelwarnschwelle, modellabhängige Leckageaktionen.

PRO / PRO L zusätzlich: Szenenauswahl und Aktivierung, Szenendauer,
Urlaubstage und Urlaub starten, Entnahmegrenzwerte, Live-Durchfluss,
Temperatur, Leckageinformationen und aktive Szene.
PRO XL zusätzlich: Live-Durchfluss, Temperatur und Leckageinformationen;
keine PRO-Szenen. Salzgewicht wird hier korrekt aus **4 Bytes** gelesen,
die Reichweite aus den folgenden 2 Bytes. Andere Modelle nutzen 2 + 2 Bytes.
XL bietet nur °dH, °fH, ppm und mmol als Härteeinheiten an.

Die Wunschwasserhärte wird mit dem dokumentierten 1-Byte-Kommando in °dH
übertragen. Zum Einstellen zuerst °dH auswählen; bei anderer Geräte-Einheit
ist der Härteregler nicht verfügbar. Der Härtesensor zeigt weiter die am
Gerät gewählte Einheit. Damit werden keine ungesicherten Einheitenumrechnungen
verwendet.

## Bewusste Grenzen der ersten Familienversion

- i-soft/i-soft K besitzen laut Tabelle Leckagealarm, keinen hier belegten
  Absperrbefehl. Die Buttons heißen deshalb „Leckagealarm setzen/zurücksetzen“.
- SAFE+-Urlaubsmodus nutzt ein anderes Bitfeld als PRO. Er wird in dieser
  Version nicht angeboten, da ein Schreiben ohne gesicherte Rücklesemöglichkeit
  andere Schutzoptionen überschreiben könnte. Bedienung weiter am Gerät.
- Die SAFE+/klassischen Tabellen vertauschen bei 3F/40 die Bezeichnungen und
  Einheiten und dokumentieren keine Rücklesefunktion. Diese Grenzwerte werden
  dort deshalb nicht als Regler angeboten. PRO hat eindeutige Angaben und
  Rücklesen; PRO XL dokumentiert diese Grenzwertkommandos nicht.
- Kommando 3E ist ein Byte: angebotene Zeiten maximal 255 Minuten.
- „Leckageschutz Position (abgeleitet)“ wird aus dem Leckagegrund berechnet,
  ist keine separat gemessene Ventilstellung.
- Historische Tages-/Wochen-/Monats-/Jahresstatistiken, Serviceadresse und
  Salzvorrat-Schreiben sind noch nicht als eigene Bedienpunkte eingebaut.
- Kein Zugriff auf ein echtes Gerät oder eine laufende Home-Assistant-Instanz
  im Erstellungssystem. Der Testumfang ist unten ausdrücklich abgegrenzt.

## Dashboard

`dashboard.yaml` ist eine Basisvorlage für alle Modelle. Ersetze darin
`judo_isoft_pro_192_168_1_50` durch den tatsächlichen Präfix deiner Entitäten.
Bei abweichendem Port enthält der neue Präfix zusätzlich `_pPORT`.
Bereits registrierte Entitäten behalten ihre bisherigen IDs; diese im
Gerätebildschirm prüfen und bei Bedarf in der Vorlage anpassen.
Die Buttons in einer Entities-Karte rufen ihre Integrationsaktion direkt auf.
`dashboard-pro.yaml` enthält das bisherige PRO-Dashboard, ebenfalls mit
anzupassenden Beispiel-IDs; es ist kein universelles Familien-Dashboard.
Ein bestehendes Dashboard muss für ein PRO-Update nicht ersetzt werden.

## Kommunikation und Prüfung

Basiswerte alle 2 Minuten; PRO/XL-Status zusätzlich alle 100 Sekunden.
Alle Anfragen eines Geräts sind serialisiert, mindestens eine Sekunde Abstand.
Leseanfragen können bei Transportfehlern einmal wiederholt werden.
Schreibanfragen werden nach Timeout **nicht automatisch wiederholt**, da das
Gerät die Aktion bereits ausgeführt haben könnte.

`python3 -m unittest discover -s tests -v` prüft Modellzuordnung,
Salzformate, Statusdecodierung, Plattformauswahl, modellabhängige Befehle,
Payloads und Fehlerverhalten mit simulierten Antworten.
Die Tests verwenden kleine Home-Assistant-Schnittstellenattrappen; sie ersetzen
keinen Installationstest mit Home Assistant und echter Gerätefirmware.

## GitHub-Repository

Vorgesehener Repository-Name: `JUDO-Home-Assistant-Integration`

- Repository: https://github.com/JUDO1936/JUDO-Home-Assistant-Integration
- Issues: https://github.com/JUDO1936/JUDO-Home-Assistant-Integration/issues

Die Dateien sind für diesen Namen vorbereitet. Das Repository muss auf GitHub
noch entsprechend benannt werden. Bei einem anderen GitHub-Benutzernamen
sind `documentation` und `issue_tracker` in `manifest.json` sowie die Links
in dieser README anzupassen.

Lade den **Inhalt** dieses Projektordners ins Repository hoch, sodass
`hacs.json`, `README.md` und `custom_components` direkt im Repository-Stamm
liegen. Der interne Ordner und die Domain `judo_isoft_pro` bleiben erhalten,
damit bestehende Installationen und Entity-IDs kompatibel bleiben.
Der neue Anzeigename erweitert nicht die unterstützten Produktfamilien;
diese Version ist weiterhin für die oben aufgeführten i-soft-Geräte bestimmt.
