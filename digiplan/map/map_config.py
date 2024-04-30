"""Actual map setup is done here."""
import dataclasses

from django.utils.translation import gettext_lazy as _
from django_mapengine import legend


@dataclasses.dataclass
class SymbolLegendLayer(legend.LegendLayer):
    """Adds symbol field."""

    symbol: str = "rectangle"


# TODO(Josi): Add real descriptions for layer info buttons
# https://github.com/rl-institut-private/digiplan/issues/249
LEGEND = {
    _("Renewables"): [
        SymbolLegendLayer(
            _("Windenergie"),
            _(
                "Windenergieanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen aus dem "
                "Marktstammdatenregister",
            ),
            layer_id="wind",
            color="#6A89CC",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Aufdach-PV"),
            _(
                "PV-Aufdachanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen aus dem "
                "Marktstammdatenregister",
            ),
            layer_id="pvroof",
            color="#FFD660",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Freiflächen-PV (Punkte)"),
            _(
                "PV-Freiflächenanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen aus dem "
                "Marktstammdatenregister",
            ),
            layer_id="pvground",
            color="#EFAD25",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Wasserkraft"),
            _(
                "Wasserkraftanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen aus dem "
                "Marktstammdatenregister",
            ),
            layer_id="hydro",
            color="#A9BDE8",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Biomasse"),
            _(
                "Biomasseanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen aus dem "
                "Marktstammdatenregister",
            ),
            layer_id="biomass",
            color="#52C41A",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Verbrennungskraftwerk"),
            _(
                "Verbrennungskraftwerke - Punktdaten realisierter oder in Betrieb befindlicher Anlagen aus dem "
                "Marktstammdatenregister",
            ),
            layer_id="combustion",
            color="#E6772E",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Geo- oder Solarthermie-, Grubengas- und Klärschlamm-Anlagen"),
            _(
                "Geo- oder Solarthermie-, Grubengas- und Klärschlamm-Anlagen - Punktdaten realisierter oder in "
                "Betrieb befindlicher Anlagen aus dem Marktstammdatenregister",
            ),
            layer_id="gsgk",
            color="#C27BA0",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Batteriespeicher"),
            _(
                "Batteriespeicher - Punktdaten realisierter oder in Betrieb befindlicher Anlagen aus dem "
                "Marktstammdatenregister",
            ),
            layer_id="storage",
            color="#8D2D5F",
            symbol="circle",
        ),
    ],
    _("Settlements Infrastructure"): [
        legend.LegendLayer(
            _("Siedlungsgebiete"),
            _(
                "Eine Siedlung ist ein Gebiet, welches die menschliche Niederlassung in beliebiger Form der "
                "gruppierten Behausung beschreibt. Sie beinhaltet überwiegend Wohngebiete.",
            ),
            layer_id="pv_ground_criteria_settlements",
        ),
        legend.LegendLayer(
            _("Siedlungsgebiete (200m Puffer)"),
            _(
                "Eine Siedlung ist ein Gebiet, welches die menschliche Niederlassung in beliebiger Form der "
                "gruppierten Behausung beschreibt. Sie beinhaltet überwiegend Wohngebiete.",
            ),
            layer_id="pv_ground_criteria_settlements_200m",
        ),
        legend.LegendLayer(
            _("Industry"),
            _(
                "Industrie- und Gewerbegebiete werden ausgewiesen, um störende Einwirkungen von Betrieben wie Lärm, "
                "Geruch oder Gefahren auf Wohnbebauung zu vermeiden.",
            ),
            layer_id="industry",
        ),
        legend.LegendLayer(
            _("Road"),
            _("Zu den Straßen gehören unter anderem Bundesautobahnen, Bundesfern-, Landes- und Kreisstraßen."),
            layer_id="road_default",
        ),
        legend.LegendLayer(
            _("Railway"),
            _(
                "Der Bahnverkehr ist ein wichtiger Bestandteil der Verkehrsinfrastruktur. Berücksichtigt "
                "werden Fernverkehrsbahnen, Regionalverkehrsbahnen und S-Bahnen.",
            ),
            layer_id="railway",
        ),
        legend.LegendLayer(
            _("Luftverkehr"),
            _(
                "Zur Infrastruktur des Luftverkehrs gehören neben Start- und Landebahnen die "
                "Flughafengebäude und Hangars.",
            ),
            layer_id="pv_ground_criteria_aviation",
        ),
        legend.LegendLayer(
            _("Air Traffic"),
            _("Ein Drehfunkfeuer ist ein Funkfeuer für die Luftfahrtnavigation."),
            layer_id="air_traffic",
        ),
        legend.LegendLayer(
            _("Militärgebiete"),
            _("Zu den militärisch genutzten Flächen gehören militärische Sperrgebiete und Liegenschaften."),
            layer_id="military",
        ),
        legend.LegendLayer(
            _("Grid"),
            _(
                "Zum Übertragungsnetz zählen die elektrischen Leitungen sowie die dazugehörigen Einrichtungen "
                "wie Schalt- und Umspannwerke der Höchst- und Hochspannungsebenen.",
            ),
            layer_id="grid",
        ),
    ],
    _("Nature Landscape"): [
        legend.LegendLayer(
            _("Naturschutzgebiete"),
            _(
                "Naturschutzgebiete dienen dem Schutz der Natur und Landschaft. Sie tragen zur Erhaltung, Entwicklung "
                "und Wiederherstellung der Lebensstätte für bestimmte wild lebende Tier- und Pflanzenarten bei. Aber "
                "auch aus wissenschaftlichen, naturgeschichtlichen und ästhetischen Gründen werden Teile oder die "
                "Gesamtheit der Natur in Schutz genommen.",
            ),
            layer_id="nature_conservation_area",
        ),
        legend.LegendLayer(
            _("Trinkwasserschutzgeb."),
            _(
                "Wasserschutzgebiete stellen die öffentliche Wasserversorgung durch die Vermeidung "
                "schädlicher Eintragungen in die Gewässer (Grundwasser, oberirdische Gewässer, Küstengewässer) sicher.",
            ),
            layer_id="drinking_water_protection_area",
        ),
        legend.LegendLayer(
            _("Fauna-Flora-Habitate"),
            _(
                "Die Fauna-Flora-Habitat-Richtlinie ist eine Naturschutz-Richtlinie der Europäischen Union (EU), die "
                "seltene oder bedrohte Arten und Lebensräume schützt. Sie gehört zum Schutzgebietsnetz Natura 2000.",
            ),
            layer_id="fauna_flora_habitat",
        ),
        legend.LegendLayer(
            _("Special Protection Area"),
            _(
                "Die Vogelschutzrichtlinie der Europäischen Union (EU) dient der Erhaltung der wild lebenden, "
                "heimischen Vogelarten. Sie regelt den Schutz dieser Vögel, ihrer Eier und Lebensräume wie Brut-, "
                "Rast- und Überwinterungsgebiete. Die Vogelschutzgebiete gehören zum Schutzgebietsnetz Natura 2000.",
            ),
            layer_id="special_protection_area",
        ),
        legend.LegendLayer(
            _("Biosphere Reserve"),
            _(
                "Biosphärenreservate sind großräumige und für bestimmte Landschaftstypen charakteristische Gebiete "
                "mit interdisziplinärem Ansatz. In diesen von der UNESCO initiierten Modellregionen soll nachhaltige "
                "Entwicklung in ökologischer, ökonomischer und sozialer Hinsicht exemplarisch verwirklicht werden. "
                "Die Biosphärenreservate sind in drei Zonen eingeteilt: Eine naturschutzorientierte Kernzone "
                "(Schutzfunktion), eine am Landschaftsschutz orientierte Pflegezone (Forschungs- und Bildungsfunktion)"
                " und eine sozioökonomisch orientierte Entwicklungszone (Entwicklungsfunktion).",
            ),
            layer_id="biosphere_reserve",
        ),
        legend.LegendLayer(
            _("Naturparke"),
            _(
                "text about nature parks.",
            ),
            layer_id="nature_park",
        ),
        legend.LegendLayer(
            _("Biotope"),
            _(
                "text for biotopes",
            ),
            layer_id="pv_ground_criteria_biotope",
        ),
        legend.LegendLayer(
            _("Waldgebiete"),
            _(
                "Wald umfasst eine Vielzahl an mit Bäumen und anderer Vegetation bedeckten Fläche "
                "mit unterschiedlicher forstwirtschaftlicher Nutzung und ökologischer Bedeutung. Wälder können in "
                "Nadel-, Laub- und Mischwald sowie anhand der Waldfunktionen (z. B. Schutzwald, Erholungswald) "
                "unterschieden werden.",
            ),
            layer_id="forest",
        ),
        legend.LegendLayer(
            _("Gewässer 1. Ordnung"),
            _(
                "Ein Gewässer ist in der Natur fließendes oder stehendes Wasser. "
                "Dazu gehören der Wasserkörper, das Gewässerbett und der Grundwasserleiter.",
            ),
            layer_id="water_first_order",
        ),
        legend.LegendLayer(
            _("Stillgewässer"),
            _(
                "Ein Gewässer ist in der Natur fließendes oder stehendes Wasser. "
                "Dazu gehören der Wasserkörper, das Gewässerbett und der Grundwasserleiter.",
            ),
            layer_id="water_bodies",
        ),
        legend.LegendLayer(
            _("Moor"),
            _(
                "text for moors",
            ),
            layer_id="moor",
        ),
        legend.LegendLayer(
            _("Überschwemmungsgeb."),
            _(
                "Bei Überschwemmungsgebieten handelt es sich um die Flächen, "
                "die statistisch gesehen mindestens einmal in hundert Jahren überflutet sein können.",
            ),
            layer_id="floodplain",
        ),
        legend.LegendLayer(
            _("Landschaftsschutzgeb."),
            _(
                "Landschaftsschutzgebiete sind oft großflächiger angelegt und zielen auf den Erhalt des "
                "Landschaftscharakters, das allgemeine Erscheinungsbild der Landschaft und dessen Schönheit ab. "
                "Sie haben einen geringeren Schutzstatus als etwa Naturschutzgebiete oder Nationalparke und "
                "unterliegen daher weniger strengen Nutzungsbeschränkungen.",
            ),
            layer_id="landscape_protection_area",
        ),
        legend.LegendLayer(
            _("Freiraumverbund"),
            _(
                "text for open spaces",
            ),
            layer_id="pv_ground_criteria_open_spaces",
        ),
    ],
    _("Negativkriterien PV"): [
        legend.LegendLayer(
            _("[N01] Siedlungsgebiete"),
            _(
                "'Siedlungsgebiete sowie Flächen rechtskräftiger Bebauungspläne mit Ausweisungen von Wohn-, "
                "Mischgebieten' - Negativkriterium [N 01] aus Kriteriengerüst PV-Freiflächenanlagen: Der tatsächliche "
                "Siedlungsbestand im Innen- und Außenbereich nach §§ 2 - 7 BauNVO also im Zusammenhang bebaute "
                "Innenbereiche, bebaute Flächen im Außenbereich, geplante Baugebiete und Siedlungsflächen nach § 30 "
                "und § 34 BauGB ist fachrechtlich ausgeschlossen.",
            ),
            layer_id="pv_ground_criteria_settlements",
        ),
        legend.LegendLayer(
            _("[N02] Siedlungsgebiete (200m Puffer)"),
            _(
                "'Abstandszone zu Siedlungsgebieten und sonstigen geschützten Nutzungen' - Negativkriterium [N 02] aus "
                "Kriteriengerüst PV-Freiflächenanlagen: Um eine räumliche Fragmentierung zu vermeiden, "
                "sind solartechnische Anlagen einerseits in räumlicher Anbindung an Siedlungsgebiete zu errichten. "
                "Andererseits wird zum Schutz vor Beeinträchtigungen z.B. durch Blendwirkungen ein 200 m Abstand zu "
                "Wohnbauflächen nach §§ 2 bis 7 BauNVO berücksichtigt. Die Abstandszone soll eine Siedlungsentwicklung "
                "der Gemeinde ermöglichen und Immissionen vorbeugen. Gemeinden können im Rahmen Ihrer kommunalen "
                "Planungshoheit geeignete Flächen auch unterhalb der 200 m für die solare Energie- und Wärmeerzeugung "
                "auf Freiflächen zur Verfügung stellen.",
            ),
            layer_id="pv_ground_criteria_settlements_200m",
        ),
        legend.LegendLayer(
            _("[N03] Überschwemmungsgeb."),
            _(
                "'100-jährliches Hochwasser HQ100 sowie festgesetzte Überschwemmungsgebiete' - Negativkriterium [N 03] "
                "aus Kriteriengerüst PV-Freiflächenanlagen: Aus § 76 Abs. 1 WHG geht hervor, "
                "dass Überschwemmungsgebiete Flächen umfassen, die bei Hochwasser überschwemmt, durchflossen oder die "
                "für Hochwasserentlastung oder Rückhaltung beansprucht werden. Nach § 78 Abs. 4 WHG ist die "
                "Errichtung oder Erweiterung baulicher Anlagen in Überschwemmungsgebieten untersagt. Festgesetzte "
                "sowie vorläufig gesicherte Überschwemmungsgebiete sind nicht als Standorte für solartechnische "
                "Anlagen geeignet (MLUK 2021, S. 6). In von Hochwasser bedrohten Gebieten ist der Hochwasserschutz "
                "gem. § 78 WHG ein besonderer Belang. Diese Flächen werden aufgrund hoher Schadensrisiken ("
                "Risikogebiete nach § 73 WHG) und Schutzanforderungen (Schutzvorschriften nach § 78 WHG) der "
                "Sicherheit des Hochwasserschutzes vom Planer als untauglich für die PV-FFA bewertet.",
            ),
            layer_id="floodplain",
        ),
        legend.LegendLayer(
            _("[N04] Freiraumverbund"),
            _(
                "'Vorranggebiet Freiraumverbund Z 6.2 LEP HR' - Negativkriterium [N 04] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: Der landesplanerisch festgelegte Freiraumverbund nach Z 6.2 LEP HR im Maßstab "
                "1:300 000 umfasst in der rechtskräftig abgegrenzten Gebietskulisse hochwertige Freiräume mit "
                "besonders hochwertigen Funktionen, die gesichert werden sollen. Gemäß Z 6.2 LEP HR ist die Kulisse "
                "des Freiraumverbundes nicht vereinbar mit der PV-FFA.",
            ),
            layer_id="pv_ground_criteria_open_spaces",
        ),
        legend.LegendLayer(
            _("[N05] Naturschutzgebiete"),
            _(
                "'Naturschutzgebiete' - Negativkriterium [N 05] aus Kriteriengerüst PV-Freiflächenanlagen. Gemäß § 23 "
                "Abs.1 BNatSchG sind rechtsverbindlich festgesetzte NSG „Gebiete, in denen ein besonderer Schutz von "
                "Natur und Landschaft in ihrer Ganzheit oder einzelnen Teilen erforderlich ist“. Eine Errichtung von "
                "Photovoltaikanlagen in den Schutzkategorien nach § 23 BNatschG ist durch Zugriffsverbote "
                "fachrechtlich ausgeschlossen.",
            ),
            layer_id="nature_conservation_area",
        ),
        legend.LegendLayer(
            _("[N06] Fauna-Flora-Habitate"),
            _(
                "'Fauna-Flora-Habitat-Gebiete' - Negativkriterium [N 06] aus Kriteriengerüst PV-Freiflächenanlagen: "
                "Die Errichtung von Photovoltaikanlagen in Flora-Fauna-Habitat-Gebieten (FFH-Gebieten), die nach der "
                "Richtlinie 92/43/EWG als besondere Gebiete von gemeinschaftlicher Bedeutung ausgewiesen sind, "
                "ist ausgeschlossen, da das Vorhaben in der Regel nicht mit dem Schutzzweck in Einklang steht bzw. in "
                "Einklang gebracht werden kann.",
            ),
            layer_id="fauna_flora_habitat",
        ),
        legend.LegendLayer(
            _("[N07] Biotope"),
            _(
                "'Gesetzlich geschützte Biotope' - Negativkriterium [N 07] aus Kriteriengerüst PV-Freiflächenanlagen: "
                "Die Errichtung von PV-FFA in Gebieten mit gesetzlich (besonders) geschützten Biotopen nach § 30 "
                "BNatschG ist fachrechtlich ausgeschlossen, da das Vorhaben mit dem Schutzzweck nicht vereinbar ist "
                "bzw. nicht in Einklang gebracht werden kann.",
            ),
            layer_id="pv_ground_criteria_biotope",
        ),
        legend.LegendLayer(
            _("[N08] Moorböden"),
            _(
                "'Naturnahe Moorböden' - Negativkriterium [N 08] aus Kriteriengerüst PV-Freiflächenanlagen: Eine hohe "
                "Naturnähe ist gegeben, wenn abgelagerte Torfschichten weitgehend menschlich unbeeinflusst sind ("
                "LaPro, Schutzgut Boden, S.2). Naturnahe Moorböden gelten aufgrund ihrer besonderen Klimarelevanz "
                "nicht als geeignete Flächen für die Errichtung von PV-FFA. „Der Erhalt der naturnahen Moorflächen "
                "und die Sicherung ihrer natürlichen Entwicklung haben höchste Priorität. Dies dient gleichzeitig dem "
                "gesetzlichen Auftrag zur Erhaltung oder Wiederherstellung eines günstigen Erhaltungszustandes der "
                "Moorlebensraumtypen gemäß FFH-Richtlinie.“ (Nationale Moorschutzstrategie, S. 10).",
            ),
            layer_id="moor",
        ),
        legend.LegendLayer(
            _("[N09] Trinkwasserschutzgeb."),
            _(
                "'Schutzzone I und II der Trinkwasserschutzgebiete' - Negativkriterium [N 09] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: In Trinkwasserschutzgebieten hat die dauerhafte Sicherung der "
                "Wasserversorgung Vorrang vor anderen Nutzungsansprüchen, die den Zielen des Trinkwasserschutzes "
                "widersprechen. In Trinkwasserschutzgebieten sollen hohe Grundwasserneubildungsraten sowie die "
                "Versickerung des Niederschlagswassers gewährleistet werden. In Zone I (Fassungsbereich) sind "
                "jegliche anderweitige Nutzung und das Betreten für Unbefugte verboten. In Zone II (engere "
                "Schutzzone) sind die Verletzung der Deckschicht und damit die Bebauung der Flächen verboten. "
                "Folglich sind festgesetzte Wasserschutzgebiete nach § 15 BbgWG i.V.m. §§ 51 und 52 WHG der "
                "Schutzzonen 1 und 2 nicht als Standorte für solartechnische Anlagen geeignet (GA PV-FFA, "
                "S.18). Gemäß §§ 51, 52 WHG i. V. mit § 15 BbgWG gelten in den festgesetzten Trinkwasserschutzzonen I "
                "und II ein Verbot bzw. eine wesentliche Beschränkung der Errichtung und Erweiterung von baulichen "
                "Anlagen.",
            ),
            layer_id="drinking_water_protection_area",
        ),
        legend.LegendLayer(
            _("[N10] Fließgewässer"),
            _(
                "'Natürliche oberirdische Gewässer' - Negativkriterium [N 10] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: Seen und Teiche besitzen vielfältige Funktionen für Landschaft und "
                "Wasserhaushalt. Sie erhöhen die Strukturvielfalt, bieten Lebensraum für zahlreiche Tier- und "
                "Pflanzenarten, können als Trittsteine im Biotopverbund dienen oder als Wasser- und Stoffspeicher "
                "wirken. Gemäß § 36 Abs. 3 Wasserhaushaltsgesetz (WHG) darf eine PV-FFA nicht errichtet und betrieben "
                "werden: in und über einem oberirdischen Gewässer, das kein künstliches oder erheblich verändertes "
                "Gewässer ist, sowie in und über einem künstlichen oder erheblich veränderten Gewässer, "
                "wenn ausgehend von der Linie des Mittelwasserstandes, die Anlage mehr als 15 Prozent der "
                "Gewässerfläche bedeckt oder der Abstand zum Ufer weniger als 40 m beträgt (GA PV-FFA, S.18).",
            ),
            layer_id="water_first_order",
        ),
        legend.LegendLayer(
            _("[N10] Stillgewässer"),
            _(
                "'Natürliche oberirdische Gewässer' - Negativkriterium [N 10] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: Seen und Teiche besitzen vielfältige Funktionen für Landschaft und "
                "Wasserhaushalt. Sie erhöhen die Strukturvielfalt, bieten Lebensraum für zahlreiche Tier- und "
                "Pflanzenarten, können als Trittsteine im Biotopverbund dienen oder als Wasser- und Stoffspeicher "
                "wirken. Gemäß § 36 Abs. 3 Wasserhaushaltsgesetz (WHG) darf eine PV-FFA nicht errichtet und betrieben "
                "werden: in und über einem oberirdischen Gewässer, das kein künstliches oder erheblich verändertes "
                "Gewässer ist, sowie in und über einem künstlichen oder erheblich veränderten Gewässer, "
                "wenn ausgehend von der Linie des Mittelwasserstandes, die Anlage mehr als 15 Prozent der "
                "Gewässerfläche bedeckt oder der Abstand zum Ufer weniger als 40 m beträgt (GA PV-FFA, S.18).",
            ),
            layer_id="water_bodies",
        ),
        legend.LegendLayer(
            _("[N11] Waldgebiete"),
            _(
                "'Waldgebiete' - Negativkriterium [N 11] aus Kriteriengerüst PV-Freiflächenanlagen: Gemäß § 1 BWaldG "
                "ist der Wald zu erhalten, erforderlichenfalls zu mehren und seine ordnungsgemäße Bewirtschaftung "
                "nachhaltig zu sichern. Wald im Sinne des § 2 LWaldG ist für die Errichtung von PV-FFA fachrechtlich "
                "ausgeschlossen. (GA PV-FFA, S.18)",
            ),
            layer_id="forest",
        ),
        legend.LegendLayer(
            _("[N12] Flächennaturdenkmale"),
            _(
                "'Flächennaturdenkmale' - Negativkriterium [N 12] aus Kriteriengerüst PV-Freiflächenanlagen: "
                "Naturdenkmale sind gemäß § 28 BNatSchG bundesweit geschützt. Sie dürfen nicht verändert werden ("
                "Veränderungsverbot). Eine Bebauung ist auszuschließen. Der Schutz begründet sich durch die "
                "Seltenheit, Eigenart oder Schönheit des Naturdenkmals sowie seinen Wert für Wissenschaft, "
                "Heimatkunde und Naturverständnis. Die Errichtung von PV-FFA in Gebieten mit flächenhaften "
                "Naturdenkmalen nach § 1 Abs. 6 Nr. 5 BauGB ist ausgeschlossen, da das Vorhaben dem Schutzzweck nicht "
                "entspricht oder mit ihm nicht in Einklang gebracht werden kann.",
            ),
            layer_id="pv_ground_criteria_nature_monuments",
        ),
        legend.LegendLayer(
            _("[N13] Luftverkehr"),
            _(
                "'Betriebsflächen von regionalen Flugplätzen' - Negativkriterium [N 13] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: Gemäß § 6 LuftVG stehen die Betriebsflächen von regionalen Flugplätzen ("
                "Flughäfen, Landeplätze und Segelfluggelände) für PV-FFA aus rechtlichen Gründen nicht zur Verfügung. "
                "Die Flächen der Verkehrs- und Sonderlandeplätze, insbesondere der gewidmeten Landebahnen gemäß § 6 "
                "LuftVG und Schutzbereiche, sind für die luftverkehrliche Nutzung freizuhalten.",
            ),
            layer_id="pv_ground_criteria_aviation",
        ),
        legend.LegendLayer(
            _("[N14] Militärgebiete"),
            _(
                "'Militärische Bereiche, deren Betreten verboten ist' - Negativkriterium [N 14] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: In der Region Oderland-Spree befinden sich zwei militärische "
                "Verteidigungsanlagen mit Schutzbereichen. Dies sind die Schutzbereiche der Verteidigungsanlagen "
                "Limsdorf und Schneeberg. Diese Gebiete sind für eine PV-FFA nur in Ausnahmefällen geeignet (§ 3 "
                "Schutzbereichsgesetz).",
            ),
            layer_id="military",
        ),
        legend.LegendLayer(
            _("[N15] Vorzug klimarobustes Ackerland"),
            _(
                "'Böden mit einem hohen Erfüllungsgrad ihrer Bodenfunktion und besonders klimarobuste Böden' - "
                "Negativkriterium [N 15] aus Kriteriengerüst PV-Freiflächenanlagen: Bodenfunktionen nach § 2 BBodSchG "
                "gelten als besonders schutzwürdig. „Flächenneuinanspruchnahmen sind auf weniger schutzwürdige und "
                "empfindliche Böden zu lenken.“ (GA PV-FFA, S.18) Der Boden erfüllt natürliche Funktionen als "
                "Lebensgrundlage und Lebensraum für Menschen, Tiere, Pflanzen und Bodenorganismen und als Bestandteil "
                "des Naturhaushalts, insbesondere mit seinen Wasser- und Nährstoffkreisläufen, so wie Abbau-, "
                "Ausgleichs- und Aufbaumedium für stoffliche Einwirkungen auf Grund der Filter-, Puffer- und "
                "Stoffumwandlungseigenschaften, insbesondere auch zum Schutz des Grundwassers. Darüber hinaus sollen "
                "die landwirtschaftlich genutzten Böden nachhaltig gesichert werden. (LaPro, 2.2.1.) Der Ausbau von "
                "konventionellen PV-FFA auf besonders klimarobusten Böden sollte vermieden werden. (Siehe ZALF-Studie "
                "auf der Website der RPG)",
            ),
            layer_id="priority_climate_resistent_agri",
        ),
        legend.LegendLayer(
            _("[N15] Vorzug Dauerkultur"),
            _(
                "'Böden mit einem hohen Erfüllungsgrad ihrer Bodenfunktion und besonders klimarobuste Böden' - "
                "Negativkriterium [N 15] aus Kriteriengerüst PV-Freiflächenanlagen: Bodenfunktionen nach § 2 BBodSchG "
                "gelten als besonders schutzwürdig. „Flächenneuinanspruchnahmen sind auf weniger schutzwürdige und "
                "empfindliche Böden zu lenken.“ (GA PV-FFA, S.18) Der Boden erfüllt natürliche Funktionen als "
                "Lebensgrundlage und Lebensraum für Menschen, Tiere, Pflanzen und Bodenorganismen und als Bestandteil "
                "des Naturhaushalts, insbesondere mit seinen Wasser- und Nährstoffkreisläufen, so wie Abbau-, "
                "Ausgleichs- und Aufbaumedium für stoffliche Einwirkungen auf Grund der Filter-, Puffer- und "
                "Stoffumwandlungseigenschaften, insbesondere auch zum Schutz des Grundwassers. Darüber hinaus sollen "
                "die landwirtschaftlich genutzten Böden nachhaltig gesichert werden. (LaPro, 2.2.1.) Der Ausbau von "
                "konventionellen PV-FFA auf besonders klimarobusten Böden sollte vermieden werden. (Siehe ZALF-Studie "
                "auf der Website der RPG)",
            ),
            layer_id="priority_permanent_crops",
        ),
        legend.LegendLayer(
            _("[N15] Vorzug Grünland"),
            _(
                "'Böden mit einem hohen Erfüllungsgrad ihrer Bodenfunktion und besonders klimarobuste Böden' - "
                "Negativkriterium [N 15] aus Kriteriengerüst PV-Freiflächenanlagen: Bodenfunktionen nach § 2 BBodSchG "
                "gelten als besonders schutzwürdig. „Flächenneuinanspruchnahmen sind auf weniger schutzwürdige und "
                "empfindliche Böden zu lenken.“ (GA PV-FFA, S.18) Der Boden erfüllt natürliche Funktionen als "
                "Lebensgrundlage und Lebensraum für Menschen, Tiere, Pflanzen und Bodenorganismen und als Bestandteil "
                "des Naturhaushalts, insbesondere mit seinen Wasser- und Nährstoffkreisläufen, so wie Abbau-, "
                "Ausgleichs- und Aufbaumedium für stoffliche Einwirkungen auf Grund der Filter-, Puffer- und "
                "Stoffumwandlungseigenschaften, insbesondere auch zum Schutz des Grundwassers. Darüber hinaus sollen "
                "die landwirtschaftlich genutzten Böden nachhaltig gesichert werden. (LaPro, 2.2.1.) Der Ausbau von "
                "konventionellen PV-FFA auf besonders klimarobusten Böden sollte vermieden werden. (Siehe ZALF-Studie "
                "auf der Website der RPG)",
            ),
            layer_id="priority_grassland",
        ),
    ],
}
