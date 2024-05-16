"""Actual map setup is done here."""
import dataclasses

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_mapengine import legend, utils


@dataclasses.dataclass
class SymbolLegendLayer(legend.LegendLayer):
    """Adds symbol field."""

    symbol: str = "rectangle"


@dataclasses.dataclass
class DistillableLegendLayer(legend.LegendLayer):
    """Adds symbol field."""

    def get_color(self) -> str:
        """Return color of underlying style for given layer ID."""
        if self.color:
            return self.color
        layer_id = self.layer_id.removesuffix("_distilled")
        return utils.get_color(layer_id)

    @property
    def style(self) -> dict:
        """
        Return layer style.

        Returns
        -------
        dict
            layer style
        """
        layer_id = self.layer_id.removesuffix("_distilled")
        return utils.get_layer_style(layer_id)


LEGEND = {
    _("Renewables"): [
        SymbolLegendLayer(
            _("Windenergie (in Betrieb)"),
            _(
                "Windenergieanlagen in Betrieb, Punktdaten (Daten: RPG Oderland-Spree, Stand: 31.12.2023)"
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="rpg_ols_wind_operating",
            color="#7a9ce7",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Windenergie genehmigt)"),
            _(
                "Genehmigte Windenergieanlagen, Punktdaten (Daten: RPG Oderland-Spree, Stand: 31.12.2023)"
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="rpg_ols_wind_approved",
            color="#6A89CC",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Windenergie (geplant)"),
            _(
                "Geplante Windenergieanlagen, Punktdaten (Daten: RPG Oderland-Spree, Stand: 31.12.2023)"
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="rpg_ols_wind_planned",
            color="#526ba2",
            symbol="circle",
        ),
        DistillableLegendLayer(
            _("FF-PV (in Betrieb)"),
            _(
                "Photovoltaik-Freiflächenanlagen in Betrieb, Flächendaten (Daten: RPG Oderland-Spree, Stand: "
                "31.12.2023)"
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id=f"rpg_ols_pv_ground_operating{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("FF-PV (genehmigt)"),
            _(
                "Genehmigte Photovoltaik-Freiflächenanlagen, Flächendaten (Daten: RPG Oderland-Spree, Stand: "
                "31.12.2023)"
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id=f"rpg_ols_pv_ground_approved{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("FF-PV (geplant)"),
            _(
                "Geplante Photovoltaik-Freiflächenanlagen, Flächendaten (Daten: RPG Oderland-Spree, Stand: 31.12.2023)"
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id=f"rpg_ols_pv_ground_planned{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        SymbolLegendLayer(
            _("Aufdach-PV"),
            _(
                "PV-Aufdachanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen(Daten: "
                "Marktstammdatenregister, Stand: 08.01.2024). Achtung: Aufgrund der Verzögerung bei der Datenmeldung "
                "kann dieser Datensatz unvollständig sein."
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="pvroof",
            color="#FFD660",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Wasserkraft"),
            _(
                "Wasserkraftanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen (Daten: "
                "Marktstammdatenregister, Stand: 08.01.2024). Achtung: Aufgrund der Verzögerung bei der Datenmeldung "
                "kann dieser Datensatz unvollständig sein."
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="hydro",
            color="#A9BDE8",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Biomasse"),
            _(
                "Biomasseanlagen - Punktdaten realisierter oder in Betrieb befindlicher Anlagen (Daten: "
                "Marktstammdatenregister, Stand: 08.01.2024). Achtung: Aufgrund der Verzögerung bei der Datenmeldung "
                "kann dieser Datensatz unvollständig sein."
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="biomass",
            color="#52C41A",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Verbrennungskraftwerk"),
            _(
                "Verbrennungskraftwerke - Punktdaten realisierter oder in Betrieb befindlicher Anlagen (Daten: "
                "Marktstammdatenregister, Stand: 08.01.2024). Achtung: Aufgrund der Verzögerung bei der Datenmeldung "
                "kann dieser Datensatz unvollständig sein."
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="combustion",
            color="#E6772E",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Geo- oder Solarthermie-, Grubengas- und Klärschlamm-Anlagen"),
            _(
                "Geo- oder Solarthermie-, Grubengas- und Klärschlamm-Anlagen - Punktdaten realisierter oder in "
                "Betrieb befindlicher Anlagen (Daten: Marktstammdatenregister, Stand: 08.01.2024). Achtung: Aufgrund "
                "der Verzögerung bei der Datenmeldung kann dieser Datensatz unvollständig sein."
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="gsgk",
            color="#C27BA0",
            symbol="circle",
        ),
        SymbolLegendLayer(
            _("Batteriespeicher"),
            _(
                "Batteriespeicher - Punktdaten realisierter oder in Betrieb befindlicher Anlagen (Daten: "
                "Marktstammdatenregister, Stand: 08.01.2024). Achtung: Aufgrund der Verzögerung bei der Datenmeldung "
                "kann dieser Datensatz unvollständig sein."
                "<br><br><i>Klicke auf ein Kartenobjekt, um mehr Informationen zu erhalten.</i>",
            ),
            layer_id="storage",
            color="#8D2D5F",
            symbol="circle",
        ),
    ],
    _("Settlements Infrastructure"): [
        DistillableLegendLayer(
            _("Siedlungsgebiete"),
            _(
                "Siedlungsgebiete sowie Flächen rechtskräftiger Bebauungspläne mit Ausweisungen von Wohn-, "
                "Mischgebieten",
            ),
            layer_id=f"pv_ground_criteria_settlements{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Siedlungsgebiete (200m Puffer)"),
            _("200m-Abstandszone zu Siedlungsgebieten und sonstigen geschützten Nutzungen"),
            layer_id=f"pv_ground_criteria_settlements_200m"
            f"{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Industry"),
            _("Industrie- und Gewerbegebiete"),
            layer_id=f"industry{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Road"),
            _("Zu den Straßen gehören unter anderem Bundesautobahnen, Bundesfern-, Landes- und Kreisstraßen."),
            layer_id=f"road_default{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Railway"),
            _("Schienenwege"),
            layer_id=f"railway{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Luftverkehr"),
            _(
                "Zur Infrastruktur des Luftverkehrs gehören neben Start- und Landebahnen die "
                "Flughafengebäude und Hangars.",
            ),
            layer_id=f"pv_ground_criteria_aviation{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Air Traffic"),
            _("Ein Drehfunkfeuer ist ein Funkfeuer für die Luftfahrtnavigation."),
            layer_id=f"air_traffic{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Militärgebiete"),
            _("Zu den militärisch genutzten Flächen gehören militärische Sperrgebiete und Liegenschaften."),
            layer_id=f"military{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Grid"),
            _(
                "Zum Stromnetz zählen die elektrischen Leitungen sowie die dazugehörigen Einrichtungen "
                "wie Schalt- und Umspannwerke der Höchst- und Hochspannungsebenen.",
            ),
            layer_id=f"grid{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
    ],
    _("Nature Landscape"): [
        DistillableLegendLayer(
            _("Naturschutzgebiete"),
            _(
                "Naturschutzgebiete dienen dem Schutz der Natur und Landschaft. Sie tragen zur Erhaltung, Entwicklung "
                "und Wiederherstellung der Lebensstätte für bestimmte wild lebende Tier- und Pflanzenarten bei. Aber "
                "auch aus wissenschaftlichen, naturgeschichtlichen und ästhetischen Gründen werden Teile oder die "
                "Gesamtheit der Natur in Schutz genommen.",
            ),
            layer_id=f"nature_conservation_area{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Trinkwasserschutzgeb."),
            _(
                "Wasserschutzgebiete stellen die öffentliche Wasserversorgung durch die Vermeidung "
                "schädlicher Eintragungen in die Gewässer (Grundwasser, oberirdische Gewässer, Küstengewässer) sicher.",
            ),
            layer_id=f"drinking_water_protection_area{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Fauna-Flora-Habitate"),
            _(
                "Die Fauna-Flora-Habitat-Richtlinie ist eine Naturschutz-Richtlinie der Europäischen Union (EU), die "
                "seltene oder bedrohte Arten und Lebensräume schützt. Sie gehört zum Schutzgebietsnetz Natura 2000.",
            ),
            layer_id=f"fauna_flora_habitat{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Special Protection Area"),
            _(
                "Die Vogelschutzrichtlinie der Europäischen Union (EU) dient der Erhaltung der wild lebenden, "
                "heimischen Vogelarten. Sie regelt den Schutz dieser Vögel, ihrer Eier und Lebensräume wie Brut-, "
                "Rast- und Überwinterungsgebiete. Vogelschutzgebiete gehören zum Schutzgebietsnetz Natura 2000.",
            ),
            layer_id=f"special_protection_area{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Biosphere Reserve"),
            _(
                "Biosphärenreservate sind großräumige und für bestimmte Landschaftstypen charakteristische Gebiete "
                "mit interdisziplinärem Ansatz. In diesen von der UNESCO initiierten Modellregionen soll nachhaltige "
                "Entwicklung in ökologischer, ökonomischer und sozialer Hinsicht exemplarisch verwirklicht werden. "
                "Die Biosphärenreservate sind in drei Zonen eingeteilt: Eine naturschutzorientierte Kernzone "
                "(Schutzfunktion), eine am Landschaftsschutz orientierte Pflegezone (Forschungs- und Bildungsfunktion)"
                " und eine sozioökonomisch orientierte Entwicklungszone (Entwicklungsfunktion).",
            ),
            layer_id=f"biosphere_reserve{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Naturparke"),
            _("Naturparke"),
            layer_id=f"nature_park{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Biotope"),
            _("Gesetzlich geschützte Biotope"),
            layer_id=f"pv_ground_criteria_biotope{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Waldgebiete"),
            _(
                "Wald umfasst eine Vielzahl an mit Bäumen und anderer Vegetation bedeckten Fläche "
                "mit unterschiedlicher forstwirtschaftlicher Nutzung und ökologischer Bedeutung. Wälder können in "
                "Nadel-, Laub- und Mischwald sowie anhand der Waldfunktionen (z. B. Schutzwald, Erholungswald) "
                "unterschieden werden.",
            ),
            layer_id=f"forest{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Fließgewässer"),
            _("Natürliche oberirdische Fließgewässer"),
            layer_id=f"water_first_order{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Stillgewässer"),
            _("Natürliche oberirdische Stillgewässer"),
            layer_id=f"water_bodies{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Moorböden"),
            _("Naturnahe Moorböden"),
            layer_id=f"moor{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Überschwemmungsgeb."),
            _(
                "Bei Überschwemmungsgebieten handelt es sich um die Flächen, "
                "die statistisch gesehen mindestens einmal in hundert Jahren überflutet sein können.",
            ),
            layer_id=f"floodplain{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Landschaftsschutzgeb."),
            _(
                "Landschaftsschutzgebiete sind oft großflächiger angelegt und zielen auf den Erhalt des "
                "Landschaftscharakters, das allgemeine Erscheinungsbild der Landschaft und dessen Schönheit ab. "
                "Sie haben einen geringeren Schutzstatus als etwa Naturschutzgebiete oder Nationalparke und "
                "unterliegen daher weniger strengen Nutzungsbeschränkungen.",
            ),
            layer_id=f"landscape_protection_area{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("Freiraumverbund"),
            _(
                "Landesplanerisch festgelegter Freiraumverbund - hochwertige Freiräume mit besonders hochwertigen "
                "Funktionen, die gesichert werden sollen.",
            ),
            layer_id=f"pv_ground_criteria_open_spaces{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
    ],
    _("Negativkriterien PV"): [
        DistillableLegendLayer(
            _("[N01] Siedlungsgebiete"),
            _(
                "'Siedlungsgebiete sowie Flächen rechtskräftiger Bebauungspläne mit Ausweisungen von Wohn-, "
                "Mischgebieten' - Negativkriterium [N 01] aus Kriteriengerüst PV-Freiflächenanlagen: Der tatsächliche "
                "Siedlungsbestand im Innen- und Außenbereich nach §§ 2 - 7 BauNVO also im Zusammenhang bebaute "
                "Innenbereiche, bebaute Flächen im Außenbereich, geplante Baugebiete und Siedlungsflächen nach § 30 "
                "und § 34 BauGB ist fachrechtlich ausgeschlossen.",
            ),
            layer_id=f"pv_ground_criteria_settlements{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"pv_ground_criteria_settlements_200m"
            f"{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"floodplain{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("[N04] Freiraumverbund"),
            _(
                "'Vorranggebiet Freiraumverbund Z 6.2 LEP HR' - Negativkriterium [N 04] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: Der landesplanerisch festgelegte Freiraumverbund nach Z 6.2 LEP HR im Maßstab "
                "1:300 000 umfasst in der rechtskräftig abgegrenzten Gebietskulisse hochwertige Freiräume mit "
                "besonders hochwertigen Funktionen, die gesichert werden sollen. Gemäß Z 6.2 LEP HR ist die Kulisse "
                "des Freiraumverbundes nicht vereinbar mit der PV-FFA.",
            ),
            layer_id=f"pv_ground_criteria_open_spaces{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("[N05] Naturschutzgebiete"),
            _(
                "'Naturschutzgebiete' - Negativkriterium [N 05] aus Kriteriengerüst PV-Freiflächenanlagen. Gemäß § 23 "
                "Abs.1 BNatSchG sind rechtsverbindlich festgesetzte NSG „Gebiete, in denen ein besonderer Schutz von "
                "Natur und Landschaft in ihrer Ganzheit oder einzelnen Teilen erforderlich ist“. Eine Errichtung von "
                "Photovoltaikanlagen in den Schutzkategorien nach § 23 BNatschG ist durch Zugriffsverbote "
                "fachrechtlich ausgeschlossen.",
            ),
            layer_id=f"nature_conservation_area{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("[N06] Fauna-Flora-Habitate"),
            _(
                "'Fauna-Flora-Habitat-Gebiete' - Negativkriterium [N 06] aus Kriteriengerüst PV-Freiflächenanlagen: "
                "Die Errichtung von Photovoltaikanlagen in Flora-Fauna-Habitat-Gebieten (FFH-Gebieten), die nach der "
                "Richtlinie 92/43/EWG als besondere Gebiete von gemeinschaftlicher Bedeutung ausgewiesen sind, "
                "ist ausgeschlossen, da das Vorhaben in der Regel nicht mit dem Schutzzweck in Einklang steht bzw. in "
                "Einklang gebracht werden kann.",
            ),
            layer_id=f"fauna_flora_habitat{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("[N07] Biotope"),
            _(
                "'Gesetzlich geschützte Biotope' - Negativkriterium [N 07] aus Kriteriengerüst PV-Freiflächenanlagen: "
                "Die Errichtung von PV-FFA in Gebieten mit gesetzlich (besonders) geschützten Biotopen nach § 30 "
                "BNatschG ist fachrechtlich ausgeschlossen, da das Vorhaben mit dem Schutzzweck nicht vereinbar ist "
                "bzw. nicht in Einklang gebracht werden kann.",
            ),
            layer_id=f"pv_ground_criteria_biotope{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"moor{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"drinking_water_protection_area{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"water_first_order{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"water_bodies{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("[N11] Waldgebiete"),
            _(
                "'Waldgebiete' - Negativkriterium [N 11] aus Kriteriengerüst PV-Freiflächenanlagen: Gemäß § 1 BWaldG "
                "ist der Wald zu erhalten, erforderlichenfalls zu mehren und seine ordnungsgemäße Bewirtschaftung "
                "nachhaltig zu sichern. Wald im Sinne des § 2 LWaldG ist für die Errichtung von PV-FFA fachrechtlich "
                "ausgeschlossen. (GA PV-FFA, S.18)",
            ),
            layer_id=f"forest{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"pv_ground_criteria_nature_monuments"
            f"{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("[N13] Luftverkehr"),
            _(
                "'Betriebsflächen von regionalen Flugplätzen' - Negativkriterium [N 13] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: Gemäß § 6 LuftVG stehen die Betriebsflächen von regionalen Flugplätzen ("
                "Flughäfen, Landeplätze und Segelfluggelände) für PV-FFA aus rechtlichen Gründen nicht zur Verfügung. "
                "Die Flächen der Verkehrs- und Sonderlandeplätze, insbesondere der gewidmeten Landebahnen gemäß § 6 "
                "LuftVG und Schutzbereiche, sind für die luftverkehrliche Nutzung freizuhalten.",
            ),
            layer_id=f"pv_ground_criteria_aviation{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
            _("[N14] Militärgebiete"),
            _(
                "'Militärische Bereiche, deren Betreten verboten ist' - Negativkriterium [N 14] aus Kriteriengerüst "
                "PV-Freiflächenanlagen: In der Region Oderland-Spree befinden sich zwei militärische "
                "Verteidigungsanlagen mit Schutzbereichen. Dies sind die Schutzbereiche der Verteidigungsanlagen "
                "Limsdorf und Schneeberg. Diese Gebiete sind für eine PV-FFA nur in Ausnahmefällen geeignet (§ 3 "
                "Schutzbereichsgesetz).",
            ),
            layer_id=f"military{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"priority_climate_resistent_agri{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"priority_permanent_crops{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
        DistillableLegendLayer(
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
            layer_id=f"priority_grassland{'_distilled' if settings.MAP_ENGINE_USE_DISTILLED_MVTS else ''}",
        ),
    ],
}
