**Inhalt**

[TOC]

---
Die Verteilung von **Windenergie und Freiflächen-Photovoltaik** in
Deutschland ist ein viel diskutiertes Thema, da der Ausbau erneuerbarer
Energien für die Energiewende und das Erreichen der Klimaziele unverzichtbar ist.
Dabei stellt sich die Frage, wie gerecht die Lasten und Vorteile verteilt sind.

Während einige Regionen und Kommunen stark vom Ausbau profitieren, etwa durch
Arbeitsplätze und Gewerbesteuereinnahmen, tragen andere primär die ökologischen
und sozialen Lasten, etwa durch Landschaftsveränderungen und erhöhte Immissionen.
Diese ungleiche Verteilung führt zu Spannungen, insbesondere zwischen ländlichen
Regionen, die oft für Wind- oder Solarparks genutzt werden, und städtischen
Ballungsräumen, die den größten Energiebedarf haben. Die Frage, wie eine
**gerechte Verteilung** von Nutzen und Lasten erreicht werden kann, ist daher
zentral in der Debatte um die Akzeptanz der erneuerbaren Energien in Deutschland.

Diese Frage ist ein Untersuchungsschwerpunkt von **EmPowerPlan**.
Anhand von verschiedenen **Gerechtigkeitsmetriken** haben wir die bundesweiten
Ausbauziele für Windenergie an Land und Freiflächen-Photovoltaik verteilt und
je **Gemeinde** berechnet. Die Ergebnisse werden im Folgenden deutschlandweit
sowie für die Region **Oderland-Spree** dargelegt.

## Der Algorithmus - Wie funktioniert die Verteilung?

!!! note "Zusammenfassung"
    Der Algorithmus verteilt Wind- und PV-Anlagen so in Gitterzellen, dass
    eine gerechte Verteilung nach definierten Gerechtigkeitsmetriken erreicht
    wird. Die Flächenverteilung basiert auf Gemeinde- und Bundeslandzielen und
    berücksichtigt die Potenzialflächen, Energiebedarf, Bevölkerungsanzahl und
    spezifischen Flächenverbrauch pro Technologie.

Das Ziel des Algorithmus besteht darin, Wind- und PV-Anlagen so zu verteilen,
dass in allen Gitterzellen eine definierte Gerechtigkeitsmetrik möglichst gleich
groß ist. Das Thema Gerechtigkeit wird hierbei aus der Sicht der Verteilung
betrachtet.
Die Verteilung soll eine Gleichheit unter allen Beteiligten herstellen.
Die unterschiedlichen Gerechtigkeitsmetriken definieren bezüglich welchem
**Kriterium** diese Gleichheit hergestellt werden soll.

Wir verteilen Wind- und PV-Anlagen auf **10x10km große Gitterzellen**.
Zur Darstellung auf Gemeindeebene werden die Ergebnisse der Verteilung von den
10x10km Gitterzellen anhand der verfügbaren Potenzialfläche je Gemeinde verteilt.
Die Gesamtfläche der Gitterzellen ist für alle Gitterzellen 10000 ha mit
Ausnahme der an der Grenze von Deutschland gelegenen Gitterzellen.

Für jede Gitterzelle ist zudem die verfügbare Fläche je Technologie
($Potenzialfläche$), der durschnittliche Energiebedarf pro Jahr in MWh ($Last$)
sowie die Bevölkerungsanzahl bekannt.
Die Potentialfläche wird auf Basis von 100x100m Gitterzellen ermittelt und dann
auf 10x10km Auflösung aggregiert. Alle Einschränkungen bezüglich der
Potentialfläche beziehen sich somit auf 100x100m Auflösung.
Für jede Technologie treffen wir Annahmen zum Flächenverbrauch pro kW
installierter Leistung, woraus die benutzte Fläche abgeleitet wird.

Wenn Bundeslandflächenziele vorgegeben werden, wird der oben beschriebene
Verteilalgorithmus zuerst innerhalb der Bundesländer angewendet, bis die
Flächenziele erreicht sind.
Wenn in allen Bundesländern das Flächenziel erreicht ist, wird der
Verteilalgorithmus auf das gesamte Bundesgebiet angewendet.

---

## Gerechtigkeit - Wie haben wir gemessen?

!!! note "Zusammenfassung"
    Wir benutzen verschiedene Gerechtigkeitsmetriken als Zielfunktionen der
    Gleichverteilung. All diese Gerechtigkeitsmetriken vertreten ein anderes
    Verständnis von gerechter Verteilung.

### Gleiche Belastung: Lastnah

Die Gerechtigkeitsmetrik "Gleiche Belastung: Lastnah" hat das Ziel, die
Bevölkerung abhängig vom Stromverbrauch gleich zu belasten.
Sie ist wie folgt definiert:

$$f_{gerecht} = {benutzteFläche \over Gesamtfläche^2 * Last}$$

Dabei soll Strom möglichst an den Orten erzeugt werden, an denen er benutzt wird.
Dies birgt zusätzliche Synergieeffekte durch mögliche Kosteneinsparungen beim
Netzausbau und geringere Netzverluste.

### Gleiche Belastung: Bevölkerungsnah

Die Gerechtigkeitsmetrik "Gleiche Belastung: Bevölkerungsnah" hat das Ziel,
wenig besiedelte Gebiete gleich zu belasten und von erneuerbare Energieanlagen
freizuhalten.
Sie ist wie folgt definiert:

$$f_{gerecht} = {benutzteFläche \over Gesamtfläche^2 * Bevölkerungsanzahl}$$

Anhand der Verhältnisses an genutzter Fläche zur Gesamtfläche und der
Arealitätsziffer (die Fläche die jedem Einwohner durchschnittlich zur Verfügung
steht) werden alle Regionen gleich belastet.
Das bedeutet, dass vor allem Regionen mit hoher Bevölkerungsdichte bebaut werden.

### Gleiche Belastung: Bevölkerungsfern

Die Gerechtigkeitsmetrik "Gleiche Belastung: Bevölkerungsfern" hat das Ziel, die
Bevölkerung gleich zu Belasten.
Sie ist wie folgt definiert:

$$f_{gerecht} = {benutzteFläche * Bevölkerungsanzahl \over Gesamtfläche^2}$$

Dabei sollen möglichst wenige Menschen durch erneuerbare Energieanlagen
beeinträchtigt werden. Das bedeutet, dass vor allem Regionen mit geringer
Bevölkerungsdichte bebaut werden.

### Gleicher Anteil an Gesamtfläche

Die Gerechtigkeitsmetrik "Gleicher Anteil an Gesamtfläche" hat das Ziel, überall
denselben Anteil an Gesamtfläche der Gitterzelle zu Nutzen.
Sie ist wie folgt definiert:

$$f_{gerecht} = {benutzteFläche \over Gesamtfläche}$$

Angelehnt an die Methodik des 2 % Flächenziels für Windenergie nutzt jede Region
den gleichen Anteil an Fläche zur Gesamtfläche für den EE-Ausbau.

### Gleicher Anteil an Potentialfläche

Die Gerechtigkeitsmetrik "Gleicher Anteil an Potentialfläche" hat das Ziel,
überall denselben Anteil an Potentialfläche zu nutzen.
Sie ist wie folgt definiert:

$$f_{gerecht} = {benutzteFläche \over Potentialfläche}$$

Dabei werden vor allem Regionen mit hoher verfügbarer Potenzialfläche bebaut.
Die Definition der Potenzialfläche spielt eine entscheidende Rolle.

---

## Szenarien - Welche Annahmen haben wir zugrunde gelegt?

!!! note "Zusammenfassung"
    - **Windenergie:** Es werden 160 GW Leistung verteilt unter Berücksichtigung
      der Bundesländerziele nach
      [WindBG](https://www.gesetze-im-internet.de/windbg/).
    - **Freiflächen-PV:** Es werden 207 GW Leistung verteilt, die Ziele für die
      Bundesländer werden aus dem
      [Netzentwicklungsplan]((https://www.netzentwicklungsplan.de/sites/default/files/2024-07/Szenariorahmenentwurf_NEP2037_2025_1.pdf))
      abgeleitet. Hierbei werden sowohl "klassische", niedrig aufgeständerte
      Anlagen als auch Agri-PV berücksichtigt.

### Wind-Szenario <img src="/static/images/icons/wind_outlined.svg" width="25" alt="">

Das Wind-Szenario hat ein Gesamtausbauziel von 160 GW installierter Leistung.
Dabei handelt es sich um die nach
[Langfristszenario](https://langfristszenarien.de/enertile-explorer-de/szenario-explorer/)
notwendige Gesamtleistung für Deutschland für das Jahr 2045.
Es wird ein Flächenverbrauch von 42 m<sup>2</sup>/kW angenommen.
Die Potentialfläche ist beschränkt auf Gitterzellen mit einer durchschnittliche
Windgeschwindigkeit von mindestens 7,17 m/s auf 160 m Höhe.
Der Abstand zu Siedlungen muss mindestens 400 m betragen.
Landschaftsschutzgebiete und Waldgebiete sind in der Potentialfläche enthalten.
Es werden die folgenden Bundeslandflächenziele nach
[WindBG](https://www.gesetze-im-internet.de/windbg/) vorgegeben:

| Bundesland             | Flächenziel (%) |
| ---------------------- | --------------- |
| Schleswig-Holstein     | 2,0             |
| Hamburg                | 0,5             |
| Niedersachsen          | 2,2             |
| Bremen                 | 0,5             |
| Nordrhein-Westfalen    | 1,8             |
| Hessen                 | 2,2             |
| Rheinland-Pfalz        | 2,2             |
| Baden-Württemberg      | 1,8             |
| Bayern                 | 1,8             |
| Saarland               | 1,8             |
| Berlin                 | 0,5             |
| Brandenburg            | 2,2             |
| Mecklenburg-Vorpommern | 2,1             |
| Sachsen                | 2,0             |
| Sachsen-Anhalt         | 2,2             |
| Thüringen              | 2,2             |

### PV-Szenario <img src="/static/images/icons/pv_low_outlined.svg" width="25" alt="">

Für das Freiflächen-PV Szenario, werden drei Technologien nacheinander verteilt.
Das Ergebnis der Verteilung von ("klassischer") **niedrig aufgeständerter PV**
ist die Ausgangslage von **bifazialer Agri-PV**, das addierte Ergebnis der
Verteilungen dieser beiden ist die Ausgangslage für die
**hochaufgeständerte Agri-PV**. Die benutzte Fläche für die Berechnung der
Gerechtigkeitsmetrik und zur Bestimmung der Bundeslandziele ist die Summe der
benutzten Fläche von aller drei Technologien. Die Abbildungen zeigen die Summe
der verteilten Kapazität über alle drei Technologien.

Es werden die folgenden Bundeslandflächenziele abgeleitet vom Szenariorahmen
des Netzentwicklungsplans
[NEP C2045](https://www.netzentwicklungsplan.de/sites/default/files/2024-07/Szenariorahmenentwurf_NEP2037_2025_1.pdf)
vorgegeben:

| Bundesland             | Flächenziel (%) |
| ---------------------- | --------------- |
| Schleswig-Holstein     | 0,9             |
| Hamburg                | 0,0             |
| Niedersachsen          | 0,6             |
| Bremen                 | 0,0             |
| Nordrhein-Westfalen    | 0,3             |
| Hessen                 | 0,4             |
| Rheinland-Pfalz        | 0,5             |
| Baden-Württemberg      | 0,5             |
| Bayern                 | 0,7             |
| Saarland               | 0,6             |
| Berlin                 | 0,0             |
| Brandenburg            | 1,0             |
| Mecklenburg-Vorpommern | 1,0             |
| Sachsen                | 0,9             |
| Sachsen-Anhalt         | 0,8             |
| Thüringen              | 0,6             |

Für die Potentialflächen der 3 Technologien benutzen wir Daten aus Kohler &
Wingenbach (2024).

| Technologie                | Ausbauziel | Flächenverbrauch       | Potentialfläche nach [Kohler & Wingenbach (2024)](#referenzen) |
|----------------------------|------------|------------------------|----------------------------------------------------------------|
| Freiflächen-PV             | 190,04 GW  | 10,0 m<sup>2</sup>/kW  | Agri-PV-Potenziale Gesamt abzüglich                            |
| (niedrig aufgeständert)    |            |                        | Agri-PV-Potenziale geringe Nutzungskonkurrenz sowie            |
|                            |            |                        | abzüglich Agri-PV-Potenziale Dauerkulturen                     |
| Bifaziale Agri-PV          | 8,64 GW    | 34,48 m<sup>2</sup>/kW | Agri-PV-Potenziale geringe Nutzungskonkurrenz                  |
|                            |            |                        | abzüglich Agri-PV-Potenziale Dauerkulturen                     |
| Hochaufgeständerte Agri-PV | 8,64 GW    | 13,51 m<sup>2</sup>/kW | Agri-PV-Potenziale Dauerkulturen                               |

---

## Ergebnisse Deutschland

!!! warning "Disclaimer"
    Die dargestellten Ergebnisse basieren auf zahlreichen Annahmen und
    überregionalen Daten. Sie können daher nicht alle regionalen Gegebenheiten
    abbilden. Sie dienen ausschließlich zu Informationszwecken und stellen
    keine gesetzlich vorgegebenen Ausbauziele oder -flächen dar!

### Windenergie <img src="/static/images/icons/wind_outlined.svg" width="25" alt="">

<a href="/static/images/equity/wind/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/wind/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

Verteilung der Windenergieleistung nach den einzelnen Gerechtigkeitsmetriken in
Gigawatt (GW) je Gemeinde.

<img src="/static/images/equity/wind/DE_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/wind/DE_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_, _Gleiche Belastung: Bevölkerungsnah_, _Gleiche Belastung: Verbrauchsnah_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die vier Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/wind/DE_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsnah_ und _Gleiche Belastung: Verbrauchsnah_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

### Freiflächen-Photovoltaik <img src="/static/images/icons/pv_low_outlined.svg" width="25" alt="">

<a href="/static/images/equity/pv/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/pv/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

Verteilung der Windenergieleistung nach den einzelnen Gerechtigkeitsmetriken in
Gigawatt (GW) je Gemeinde.

<img src="/static/images/equity/pv/DE_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/pv/DE_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_, _Gleiche Belastung: Bevölkerungsnah_, _Gleiche Belastung: Verbrauchsnah_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die vier Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/pv/DE_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsnah_ und _Gleiche Belastung: Verbrauchsnah_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

---

## Ergebnisse Oderland-Spree

!!! warning "Disclaimer"
    Die dargestellten Ergebnisse basieren auf zahlreichen Annahmen und
    überregionalen Daten. Sie können daher nicht alle regionalen Gegebenheiten
    abbilden. Sie dienen ausschließlich zu Informationszwecken und stellen
    keine gesetzlich vorgegebenen Ausbauziele oder -flächen dar!

### Windenergie

<a href="/static/images/equity/wind/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/wind/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

Verteilung der Windenergieleistung nach den einzelnen Gerechtigkeitsmetriken in
Gigawatt (GW) je Gemeinde.

<img src="/static/images/equity/wind/oder_spree_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/wind/oder_spree_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_, _Gleiche Belastung: Bevölkerungsnah_, _Gleiche Belastung: Verbrauchsnah_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die vier Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/wind/oder_spree_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsnah_ und _Gleiche Belastung: Verbrauchsnah_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

### Freiflächen-Photovoltaik

<a href="/static/images/equity/pv/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/pv/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

Verteilung der Windenergieleistung nach den einzelnen Gerechtigkeitsmetriken in
Gigawatt (GW) je Gemeinde.

<img src="/static/images/equity/pv/oder_spree_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/pv/oder_spree_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsfern_, _Gleiche Belastung: Bevölkerungsnah_, _Gleiche Belastung: Verbrauchsnah_ und _Gleicher Anteil an Gesamtfläche_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die vier Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

<img src="/static/images/equity/pv/oder_spree_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Konsensnutzung über die Gerechtigkeitsmetriken _Gleiche Belastung: Bevölkerungsnah_ und _Gleiche Belastung: Verbrauchsnah_.
Die linke Abbildung zeigt die kleinstmögliche verteilte Kapazität in [GW] pro Gemeinde über die beiden Gerechtigkeitsmetriken.
Die rechte Abbildung zeigt die Gerechtigkeitsmetrik, welche zur kleinsten Verteilmenge innerhalb der jeweiligen Gemeinde führt.

---

## Referenzen

Kohler, M., & Wingenbach, M. (2024). Potenzialflächen für Agri-Photovoltaik [Data set]. Zenodo. [https://doi.org/10.5281/zenodo.10878761](https://doi.org/10.5281/zenodo.10878761)
