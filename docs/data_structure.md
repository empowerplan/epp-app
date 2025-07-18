# Datenstruktur

Die Datenstruktur des Projekts ist in zwei Hauptbereiche unterteilt: `digiplan/data/digipipe` und `digiplan/data/oemof`. 

Der Bereich `digipipe` enthält die für die Anwendung aufbereiteten Daten in einer strukturierten Form. 
Diese Daten sind in mehrere Unterverzeichnisse organisiert:

- `captions`: Enthält JSON-Dateien mit Beschriftungen und Übersetzungen für verschiedene Datenfelder, die in der Benutzeroberfläche verwendet werden.
- `geodata`: Beinhaltet geografische Daten im GeoPackage-Format (.gpkg), die verschiedene räumliche Informationen wie Verwaltungsgrenzen, Schutzgebiete, Infrastruktur und Potenzialflächen für erneuerbare Energien darstellen.
- `scalars`: Enthält skalare Daten (Einzelwerte) für verschiedene Energieparameter.
- `sequences`: Beinhaltet zeitreihenbasierte Daten für die Energiemodellierung.
- `settings`: Enthält Konfigurationsdateien für die Anwendung, wie zum Beispiel Einstellungen für Energieparameter und Kartenebenen.

Die Struktur und Beziehungen dieser Daten sind in der Datei `datapackage_app.json` definiert, die Metadaten über alle verfügbaren Ressourcen enthält, einschließlich Beschreibungen, Pfade und Quellinformationen.

Der Bereich `oemof` enthält Daten für die Energiesystemmodellierung mit dem Open Energy Modelling Framework.
Dort können mehrere Szenarien als oemof-Datenpaket abgelegt werden. 
Im EmPowerPlan Projekt wird allerdings nur das Szenario `scenario_2045` verwendet, das folgende Struktur hat: 

- Ein `data`-Verzeichnis mit detaillierten Informationen zu Energiesystemkomponenten wie Batterien, Kraftwerken, Netzen usw.
- Eine `datapackage.json`-Datei, die die Struktur und Beziehungen der Daten im Szenario definiert.
- Zusätzliche Dateien wie `additional_scalars.csv` für ergänzende Informationen.

Diese Datenstruktur ermöglicht eine effiziente Organisation und Verarbeitung der komplexen Daten, die für die Energiesystemanalyse und -planung benötigt werden.

