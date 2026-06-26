<img src="/static/images/logos/EmPowerPlan-logo-horizontal.png" alt="EmPowerPlan Logo" style="float: right; width: 200px; margin-left: 1.5rem; margin-bottom: 0.5rem;">

**Inhalt**

[TOC]

<div style="clear: both;"></div>

## Gerechte Verteilung von Wind- und Solarenergieanlagen: Was bedeutet das?

Der Ausbau erneuerbarer Energien wie **Windkraft und Freiflächen-Photovoltaik** (Solarparks) ist entscheidend, um die Klimaziele Deutschlands zu erreichen. Doch dieser Ausbau wirft auch die Frage auf: **Wie können die Lasten und Vorteile gerecht verteilt werden?**

Während einige Regionen von den erneuerbaren Energien profitieren – zum Beispiel durch Bürgerenergiegesellschaften, Pachteinnahmen für Gemeindeflächen oder Gewerbesteuereinnahmen – sehen sich andere vor allem mit Nachteilen konfrontiert, etwa durch Eingriffe in die Landschaft oder potenzielle Belastungen wie Lärm und Schattenwurf. Diese Ungleichheit führt oft zu Spannungen, insbesondere zwischen ländlichen Regionen, in denen die Anlagen gebaut werden, und städtischen Gebieten, die den Großteil der Energie verbrauchen.

Das Forschungsprojekt EmPowerPlan hat sich zum Ziel gesetzt, Vorschläge für eine gerechtere Verteilung von Wind- und Solarenergieanlagen zu entwickeln. Im Mittelpunkt steht die Frage: Wie können alle Regionen gerecht behandelt werden?

## Der Algorithmus - Wie funktioniert die Verteilung?

Um die Anlagen möglichst gerecht zu verteilen, haben wir unterschiedliche Vorstellungen von Gerechtigkeit untersucht und diese in einem Algorithmus zusammengeführt. Dabei wurden folgende Punkte berücksichtigt:

- **Regionale Unterschiede**: Jede Gemeinde in Deutschland wurde analysiert, um ihre Eignung für Wind- oder Solarenergie zu prüfen.
- **Mehrere Gerechtigkeitskriterien**: Verschiedene Kriterien wie Bevölkerungszahl, Energieverbrauch und verfügbare Flächen wurden einbezogen.
- **Gemeinsame Lösungen**: Flächen, die mehrere Kriterien erfüllen, bieten den größten Spielraum für Entscheidungen.

Die Verteilung erfolgt auf 10 x 10 km große Gitterzellen. Der Algorithmus verteilt Wind- und PV-Anlagen so in Gitterzellen, dass eine gerechte Verteilung nach definierten Gerechtigkeitsmetriken erreicht wird. Die Flächenverteilung basiert auf Gemeinde- und Bundeslandzielen und berücksichtigt die Potenzialflächen, Energiebedarf, Bevölkerungsanzahl und spezifischen Flächenverbrauch pro Technologie.

## Welche Kriterien für Gerechtigkeit wurden genutzt?

Wir haben fünf verschiedene Ansätze für gerechte Verteilungen von EE-Anlagen untersucht (Klick auf den Ansatz zeigt die mathematische Formulierung):

<details markdown="1">
<summary><strong>1. Energieverbrauch vor Ort</strong>: Anlagen sollten dort gebaut werden, wo die Energie benötigt wird. Das spart Kosten und reduziert Energieverluste.</summary>

Die Gerechtigkeitsmetrik "Gleiche Belastung: Lastnah" hat das Ziel, die Bevölkerung abhängig vom Stromverbrauch gleich zu belasten.

Sie ist wie folgt definiert:
$$f_{gerecht} = {benutzteFläche \over Gesamtfläche^2 * Last}$$

Dabei soll Strom möglichst an den Orten erzeugt werden, an denen er benutzt wird. Dies birgt zusätzliche Synergieeffekte durch mögliche Kosteneinsparungen beim Netzausbau und geringere Netzverluste.

</details>

<details markdown="1">
<summary><strong>2. Bevölkerungsnah</strong>: Um der Bevölkerung genug Erholungsfläche zur Verfügung zu stellen, werden Regionen mit mehr Einwohnern stärker ausgebaut.</summary>

Die Gerechtigkeitsmetrik "Gleiche Belastung: Bevölkerungsnah" hat das Ziel, wenig besiedelte Gebiete gleich zu belasten und von erneuerbare Energieanlagen freizuhalten.

Sie ist wie folgt definiert:
$$f_{gerecht} = {benutzteFläche \over Gesamtfläche^2 * Bevölkerungsanzahl}$$

Anhand des Verhältnisses an genutzter Fläche zur Gesamtfläche und der Arealitätsziffer (die Fläche die jedem Einwohner durchschnittlich zur Verfügung steht) werden alle Regionen gleich belastet. Das bedeutet, dass vor allem Regionen mit hoher Bevölkerungsdichte bebaut werden.

</details>

<details markdown="1">
<summary><strong>3. Bevölkerungsfern</strong>: Anlagen könnten in Gebieten mit weniger Einwohnern konzentriert werden, um die Mehrheit der Bevölkerung zu entlasten.</summary>

Die Gerechtigkeitsmetrik "Gleiche Belastung: Bevölkerungsfern" hat das Ziel, die Bevölkerung gleich zu Belasten.

Sie ist wie folgt definiert:
$$f_{gerecht} = {benutzteFläche * Bevölkerungsanzahl \over Gesamtfläche^2}$$

Dabei sollen möglichst wenige Menschen durch erneuerbare Energieanlagen beeinträchtigt werden. Das bedeutet, dass vor allem Regionen mit geringer Bevölkerungsdichte bebaut werden.

</details>

<details markdown="1">
<summary><strong>4. Gleicher Flächenanteil</strong>: Jede Region trägt den gleichen Anteil ihrer Fläche für erneuerbare Energien bei.</summary>

Die Gerechtigkeitsmetrik "Gleicher Anteil an Gesamtfläche" hat das Ziel, überall denselben Anteil an Gesamtfläche der Gitterzelle zu Nutzen.

Sie ist wie folgt definiert:
$$f_{gerecht} = {benutzteFläche \over Gesamtfläche}$$

Angelehnt an die Methodik des 2 % Flächenziels für Windenergie nutzt jede Region den gleichen Anteil an Fläche zur Gesamtfläche für den EE-Ausbau.

</details>

<details markdown="1">
<summary><strong>5. Optimale Nutzung von Potenzialflächen</strong>: Regionen mit großen geeigneten Flächen werden stärker für den Ausbau genutzt.</summary>

Die Gerechtigkeitsmetrik "Gleicher Anteil an Potentialfläche" hat das Ziel, überall denselben Anteil an Potentialfläche zu nutzen.

Sie ist wie folgt definiert:
$$f_{gerecht} = {benutzteFläche \over Potentialfläche}$$

Dabei werden vor allem Regionen mit hoher verfügbarer Potenzialfläche bebaut. Die Definition der Potenzialfläche spielt eine entscheidende Rolle.

</details>

## Wie wurde das Zielszenario definiert?

Für unsere Analyse haben wir Szenarien für Windenergie und Freiflächen-Photovoltaik erstellt. Dabei wurden verschiedene Annahmen zugrunde gelegt:

### Windenergie <img src="/static/images/icons/wind_outlined.svg" width="25" alt="">

Insgesamt sollen **160 Gigawatt Leistung bis 2045** installiert werden [[1](#referenzen)]. Nur Gebiete mit ausreichend Windgeschwindigkeit (von mindestens 7,17 m/s auf 160 m Höhe) wurden berücksichtigt. Die Potenzialfläche []2](#referenzen)] beinhaltet alle rechtlichen und naturschutzbezogenen Ausschlussgebiete sowie Abstände zu Wohngebieten (mindestens 400 m). Als Flächenverbrauch für Windenergieanlagen wurde 42 m<sup>2</sup>/kW angenommen. Die Ausbauziele der Bundesländer [[3](#referenzen)] wurden berücksichtigt.

### Freiflächen-Photovoltaik <img src="/static/images/icons/pv_low_outlined.svg" width="25" alt="">

Ziel ist es, **207 Gigawatt Leistung bis 2045** zu installieren [[1](#referenzen)]. Hierbei wurden verschiedene Technologien wie klassische Freiflächen-PV (Flächenverbrauch 10,0 m<sup>2</sup>/kW) und Agri-Photovoltaik-Technologien (hochaufgeständert und bifazial) berücksichtigt. Hochaufgeständerte PV-Anlagen werden nach eigener Potenzialanalyse [[4](#referenzen)] vor allem auf Dauerkulturen installiert (Flächenverbrauch 13,51 m<sup>2</sup>/kW). Bifaziale PV-Anlagen werden auf Flächen mit niedriger und mittlerer Bodengüte genutzt (Flächenverbrauch 34,48 m<sup>2</sup>/kW). Ausbauziele für die Bundesländer wurden auf Basis des Netzentwicklungsplans [[5](#referenzen)] abgeleitet und berücksichtigt.

## Was sind Konsensflächen?

Da unterschiedliche **Gerechtigkeitsvorstellungen** nebeneinander bestehen, müssen wir lernen, konstruktiv mit dieser Vielfalt umzugehen. Hierbei hilft die Idee der Konsensflächen:

- **Gleichwertigkeit der Vorstellungen**: Alle Gerechtigkeitskriterien werden gleichberechtigt behandelt und übereinandergelegt.
- **Flächenüberschneidung**: Flächen, die nach allen Gerechtigkeitsvorstellungen für den Ausbau geeignet sind, gelten als Konsensflächen.
- **Verhandlungsbasis**: Diese Flächen bieten die größte Überschneidung an unterschiedlichen Gerechtigkeitsvorstellungen und sind bevorzugt für den weiteren Ausbau erneuerbarer Energien zu betrachten.
- **Keine festen Standorte**: Es werden Empfehlungen gegeben, keine verpflichtenden Ausbauorte.

Der Ansatz ermöglicht es, trotz unterschiedlicher Vorstellungen zu gemeinsamen Handlungsempfehlungen zu kommen. Das Minimum aus den verschiedenen Gerechtigkeitsvorstellungen stellt dabei die Übereinstimmung dar – eine Fläche, die als fair angesehen werden kann.

## Ergebnisse: Wie sieht die Verteilung aus für Deutschland?

!!! warning "Disclaimer"
    Die dargestellten Ergebnisse basieren auf zahlreichen Annahmen und
    überregionalen Daten. Sie können daher nicht alle regionalen Gegebenheiten
    abbilden. Sie dienen ausschließlich zu Informationszwecken und stellen
    keine gesetzlich vorgegebenen Ausbauziele oder -flächen dar!

### Windenergie <img src="/static/images/icons/wind_outlined.svg" width="25" alt="">

<a href="/static/images/equity/wind/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/wind/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

_Verteilung der Windenergieleistung nach den einzelnen Gerechtigkeitsmetriken in Gigawatt (GW) je Gemeinde._

Die Verteilung der Gesamtleistung von 160 GW unterscheidet sich je nach zugrundeliegender Gerechtigkeitsmetrik. Nach der Gerechtigkeitsvorstellung „Bevölkerungsfern" werden beispielsweise einzelne Gemeinden mit hohem Anteil an Potenzialfläche und geringer Bevölkerungsdichte stärker bebaut als in den Vergleichsszenarien.

Werden alle EE-Gleichverteilungen übereinander gelegt, so besteht eine nennenswerte Übereinstimmung über die zu nutzenden Flächen. Dieses kann als **„Konsens-Zubau-Potential"** bezeichnet werden. Hier im Beispiel können mit 77 GW etwa 48 % des Windzubaus nach diesem Ansatz konfliktfrei in die Fläche gebracht werden. Die Verteilung, die den „kleinsten gemeinsamen Nenner" bestimmt, wird am häufigsten durch die Verteilung nach „Potentialfläche" definiert.

<img src="/static/images/equity/wind/DE_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Bei einer Überlagerung von vier Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern", „Bevölkerungsnah", „Verbrauchsnah" und „Anteil an Gesamtfläche" können insgesamt rund 90 GW an Windleistung realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei allen Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über alle Gerechtigkeitsmetriken).

<img src="/static/images/equity/wind/DE_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern" und „Anteil an Gesamtfläche" können insgesamt rund 127 GW an Windleistung realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

<img src="/static/images/equity/wind/DE_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsnah" und „Verbrauchsnah" können insgesamt rund 154 GW an Windleistung realisiert werden. Mit 96 % der Gesamtleistung stellt die Überlagerung dieser beiden Gerechtigkeitsvorstellungen die größte Schnittmenge an verfügbaren Flächen dar. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

### Freiflächen-Photovoltaik <img src="/static/images/icons/pv_low_outlined.svg" width="25" alt="">

<a href="/static/images/equity/pv/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/pv/DE_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

_Verteilung der Freiflächen-PV-Leistung (klassische FF-PV plus Agri-PV) nach den einzelnen Gerechtigkeitsmetriken in Gigawatt (GW) je Gemeinde._

Die Verteilung der Gesamtleistung von 207 GW unterscheidet sich je nach zugrundeliegender Gerechtigkeitsmetrik. Nach der Gerechtigkeitsvorstellung „Bevölkerungsfern" werden beispielsweise einzelne Gemeinden mit hohem Anteil an Potenzialfläche und geringer Bevölkerungsdichte stärker bebaut als in den Vergleichsszenarien.

Werden alle EE-Gleichverteilungen übereinander gelegt, so besteht eine nennenswerte Übereinstimmung über zu nutzende Flächen. Dieses kann als „Konsens-Zubau-Potential" bezeichnet werden. Hier im Beispiel können mit 82 GW etwa 40 % des PV-Freiflächenzubaus nach diesem Ansatz konfliktfrei in die Fläche gebracht werden.

<img src="/static/images/equity/pv/DE_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Bei einer Überlagerung von vier Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern", „Bevölkerungsnah", „Verbrauchsnah" und „Anteil an Gesamtfläche" können insgesamt rund 88 GW an PV-Freiflächen-Leistung realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei allen Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über alle Gerechtigkeitsmetriken).

<img src="/static/images/equity/pv/DE_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern" und „Anteil an Gesamtfläche" können insgesamt rund 155 GW an PV-Freiflächen-Leistung realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

<img src="/static/images/equity/pv/DE_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsnah" und „Verbrauchsnah" können insgesamt rund 192 GW an PV-Freiflächen-Leistung realisiert werden. Mit 93 % der Gesamtleistung stellt die Überlagerung dieser beiden Gerechtigkeitsvorstellungen die größte Schnittmenge an verfügbaren Flächen dar. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

## Ergebnisse: Wie sieht die Verteilung aus für Oderland-Spree?

!!! warning "Disclaimer"
    Die dargestellten Ergebnisse basieren auf zahlreichen Annahmen und
    überregionalen Daten. Sie können daher nicht alle regionalen Gegebenheiten
    abbilden. Sie dienen ausschließlich zu Informationszwecken und stellen
    keine gesetzlich vorgegebenen Ausbauziele oder -flächen dar!

### Windenergie

<a href="/static/images/equity/wind/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/wind/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

_Verteilung der Windenergieleistung nach den einzelnen Gerechtigkeitsmetriken in Gigawatt (GW) für alle Gemeinden der Planungsregion „Oderland-Spree"._

Je nach zugrundeliegender Gerechtigkeitsmetrik werden von der deutschlandweiten Gesamtleistung von 160 GW unterschiedlich hohe Ausbaumengen in die Region Oderland-Spree verteilt. Die Verteilung nach der Gerechtigkeitsvorstellung „Bevölkerungsfern" führt für die Planungsregion Oderland-Spree zu dem vergleichsweise geringsten Zubauziel von 1,9 GW Windenergie. Die höchste Windleistung kommt mit 2,5 GW durch die Verteilung nach „Anteil an Potenzialfläche" zustande.

<img src="/static/images/equity/wind/oder_spree_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Werden alle EE-Gleichverteilungen übereinander gelegt, so besteht eine nennenswerte Übereinstimmung über die zu nutzenden Flächen. Dieses kann als **„Konsens-Zubau-Potential"** bezeichnet werden. Bei einer Überlagerung von vier Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern", „Bevölkerungsnah", „Verbrauchsnah" und „Anteil an Gesamtfläche" können insgesamt rund 1,3 GW an Windleistung in der Planungsregion Oderland-Spree realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei allen Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über alle Gerechtigkeitsmetriken).

<img src="/static/images/equity/wind/oder_spree_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern" und „Anteil an Gesamtfläche" können insgesamt 1,7 GW an Windleistung in der Region Oderland-Spree realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

<img src="/static/images/equity/wind/oder_spree_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsnah" und „Verbrauchsnah" können insgesamt 2,1 GW an Windleistung in der Planungsregion Oderland-Spree realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

### Freiflächen-Photovoltaik

<a href="/static/images/equity/pv/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA.png" target="_blank"><img src="/static/images/equity/pv/oder_spree_installed_capacity_gw_equalAREA-equalCLOSE2load-equalCLOSE2pop-equalPOP-equalPOTAREA_40p.png" width="100%" alt=""></a>

_Verteilung der Freiflächen-PV (klassische Freiflächen-PV plus Agri-PV) nach den einzelnen Gerechtigkeitsmetriken in Gigawatt (GW) für alle Gemeinden der Planungsregion „Oderland-Spree"._

Je nach zugrundeliegender Gerechtigkeitsmetrik werden von der deutschlandweiten Gesamtleistung von 207 GW unterschiedlich hohe Ausbaumengen in die Region Oderland-Spree verteilt. Die Verteilung nach der Gerechtigkeitsvorstellung „Bevölkerungsfern" führt für die Planungsregion Oderland-Spree zu dem vergleichsweise geringsten Zubauziel von 3,6 GW Freiflächen-PV. Die höchste Freiflächen-PV-Leistung kommt mit 5,1 GW durch die Verteilung nach „Anteil an Potenzialfläche" zustande.

<img src="/static/images/equity/pv/oder_spree_min-overlay_equalAREA-equalPOP-equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Werden alle EE-Gleichverteilungen übereinander gelegt, so besteht eine nennenswerte Übereinstimmung über zu nutzende Flächen. Dieses kann als „Konsens-Zubau-Potential" bezeichnet werden. Bei einer Überlagerung von vier Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern", „Bevölkerungsnah", „Verbrauchsnah" und „Anteil an Gesamtfläche" können insgesamt 1,6 GW an PV-Freiflächen-Leistung in der Planungsregion Oderland-Spree realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei allen Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über alle Gerechtigkeitsmetriken).

<img src="/static/images/equity/pv/oder_spree_min-overlay_equalAREA-equalPOP_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsfern" und „Anteil an Gesamtfläche" können insgesamt 3,1 GW an PV-Freiflächen-Leistung in der Planungsregion Oderland-Spree realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

<img src="/static/images/equity/pv/oder_spree_min-overlay_equalCLOSE2pop-equalCLOSE2load_40p.png" width="75%" alt="">

Bei einer Überlagerung von nur zwei Gerechtigkeitsvorstellungen wie hier im Beispiel „Bevölkerungsnah" und „Verbrauchsnah" können insgesamt 3,7 GW an PV-Freiflächen-Leistung in der Planungsregion Oderland-Spree realisiert werden. Die rechte Grafik zeigt für jede Gemeinde an, welche der beiden Gerechtigkeitsvorstellungen den kleinsten gemeinsamen Nenner definiert. In der linken Grafik wird nur die installierbare Leistung dargestellt, die bei beiden Verteilungen realisierbar ist (kleinstmögliche verteilte Kapazität in GW pro Gemeinde über beide Gerechtigkeitsmetriken).

## Wo finde ich weitere Informationen?

Die in EmPowerPlan entwickelten Methoden und Ergebnisse sind in den folgenden
Publikationen dokumentiert:

- Degel, M. et al. (2025). EmPowerPlan – Regionale Planung der Energiewende – Partizipation und Gerechtigkeit vor Ort und das große Ganze im Blick, Abschlussbericht. [https://doi.org/10.34657/21079](https://doi.org/10.34657/21079)
- Wingenbach, M. Flachsbarth, F., Aschauer, J. & Winger, C. (2025). Gerechtigkeit im EE-Ausbau: Erneuerbare gerecht in die Fläche bringen. Verteilungslogiken, algorithmische Ansätze und Konsensräume. [https://www.oeko.de/fileadmin/oekodoc/Gerechtigkeit-im-EE-Ausbau-Fl%C3%A4che.pdf](https://www.oeko.de/fileadmin/oekodoc/Gerechtigkeit-im-EE-Ausbau-Fl%C3%A4che.pdf)
- Flachsbarth, F., Wingenbach, M., & Winger, C. (2025). Gerechtigkeit im EE-Ausbau: Systemische Wirkung gerechter EE-Verteilungen. Kosten, Emissionen und Strommarktimplikationen. [https://www.oeko.de/fileadmin/oekodoc/Gerechtigkeit-im-EE-Ausbau-Systemische-Wirkung.pdf](https://www.oeko.de/fileadmin/oekodoc/Gerechtigkeit-im-EE-Ausbau-Systemische-Wirkung.pdf)
- Wingenbach, M., Flachsbarth, F., Aschauer, J., & Winger, C. (2025). EmPowerPlan EE-Regionalisierungsszenarien [Data set]. Zenodo. [https://doi.org/10.5281/zenodo.15188220](https://doi.org/10.5281/zenodo.15188220)

## Und wie geht es weiter?

Die in EmPowerPlan entwickelten Methoden zur gerechten Verteilung von Erneuerbaren Energien werden im Folgeprojekt **EEquityMap** auf ganz Deutschland ausgeweitet. Ziel ist eine interaktive, deutschlandweite Online-Karte, mit der Nutzer:innen verschiedene Gerechtigkeitsmetriken kombinieren und Ausbauszenarien für Wind- und Freiflächen-PV in Echtzeit erkunden können.

[Hier geht's zur Projektseite](https://reiner-lemoine-institut.de/projekt/eequitymap-interaktive-deutschlandweite-online-karte-zur-gerechten-verteilung-von-erneuerbaren-energien/)

## Referenzen

[1] Fraunhofer ISI (2024). Langfristszenarien 2. [https://langfristszenarien.de/enertile-explorer-de/szenario-explorer/](https://langfristszenarien.de/enertile-explorer-de/szenario-explorer/)

[2] Amme, J. (2022). Der Photovoltaik- und Windflächenrechner - Geodaten Potenzialflächen (v1.0) [Data set]. Zenodo. [https://doi.org/10.5281/zenodo.6728382](https://doi.org/10.5281/zenodo.6728382)

[3] Gesetz zur Festlegung von Flächenbedarfen und zur Genehmigungserleichterung für Windenergieanlagen an Land und für Anlagen zur Speicherung vom Strom oder Wärme aus erneuerbaren Energien in bestimmten Gebieten (Windenergieflächenbedarfsgesetz - WindBG). [https://www.gesetze-im-internet.de/windbg/](https://www.gesetze-im-internet.de/windbg/)

[4] Kohler, M., & Wingenbach, M. (2024). Potenzialflächen für Agri-Photovoltaik [Data set]. Zenodo. [https://doi.org/10.5281/zenodo.10878761](https://doi.org/10.5281/zenodo.10878761)

[5] Szenariorahmen zum  Netzentwicklungsplan Strom 2037/2045, Version 2025 - Entwurf der Übertragungsnetzbetreiber (2024). [https://www.netzentwicklungsplan.de/sites/default/files/2024-07/Szenariorahmenentwurf_NEP2037_2025_1.pdf](https://www.netzentwicklungsplan.de/sites/default/files/2024-07/Szenariorahmenentwurf_NEP2037_2025_1.pdf)
