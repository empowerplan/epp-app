//const onbaordingCloseBtn = document.getElementById("close-onboarding");

const intro_tour = new Shepherd.Tour({  // jshint ignore:line
    useModalOverlay: true,
    defaultStepOptions: {
        cancelIcon: {
            enabled: true
        },
        classes: 'class-1 class-2',
        scrollTo: {behavior: 'smooth', block: 'center'}
    }
});


intro_tour.addStep({
    title: 'Navigation',
    text: 'Schritt für Schritt zu Ihrem eigenen Szenario.',
    attachTo: {
        element: '.steps',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.cancel();
            },
            classes: 'shepherd-button-secondary',
            text: 'Tour beenden'
        },
        {
            action() {
                const statusquoDropdown = document.getElementById("situation_today");
                statusquoDropdown.value = "capacity_statusquo";
                PubSub.publish(mapEvent.CHOROPLETH_SELECTED, statusquoDropdown.value);
                return this.next();
            },
            text: 'Weiter'
        }

    ],
    id: 'start'
});

intro_tour.addStep({
    title: 'Situation heute',
    text: 'Schauen Sie sich die Situation heute an.',
    attachTo: {
        element: '#situation_today',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'situation_today'
});


intro_tour.addStep({
    title: 'Situation heute',
    text: 'Zu jeder Kategorie gibt es ein Diagramm für die Region.',
    attachTo: {
        element: '#region_chart_statusquo',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                // Hide status quo choropleth again
                const statusquoDropdown = document.getElementById("situation_today");
                statusquoDropdown.value = "";
                deactivateChoropleth();
                PubSub.publish(eventTopics.CHOROPLETH_DEACTIVATED);

                // Activate layers
                document.querySelector(".static-layer #wind").click();
                document.querySelector(".static-layer #road_default").click();
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'region_chart'
});


intro_tour.addStep({
    title: 'Karte',
    text: 'Lassen Sie sich die heutigen Anlagen und Flächen auf der Karte anzeigen.',
    attachTo: {
        element: '#js-map-layers-box',
        on: 'left'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'layer_switch'
});


intro_tour.addStep({
    title: 'Karte',
    text: 'Klicken Sie auf ein einzelnes Icon, um mehr über diese Anlage zu erfahren.',
    attachTo: {
        element: '.maplibregl-canvas',
        on: 'top'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                document.querySelector(".static-layer #wind").click();
                document.querySelector(".static-layer #road_default").click();
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'cluster_popup'
});


intro_tour.addStep({
    title: 'Nächster Schritt',
    text: 'Hier gehts weiter zu den Einstellungen.',
    attachTo: {
        element: '#menu_next_btn',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                document.getElementById("menu_next_btn").click();
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'menu_next_btn'
});

intro_tour.addStep({
    title: 'Einstellungen',
    text: 'Verändern Sie die Einstellungen, um Ihr eigenes Szenario zu erstellen.',
    attachTo: {
        element: '#panel_2_settings',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_1_today'
});

intro_tour.addStep({
    title: 'Einstellungen',
    text: 'Hier können Sie mehr ins Detail gehen.',
    attachTo: {
        element: '.c-slider__label--more',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'more_slider'
});


intro_tour.addStep({
    title: 'Einstellungen',
    text: 'Schauen Sie, wie sich die Verteilung verändert.',
    attachTo: {
        element: '.power-mix__chart',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'power_mix_chart'
});


intro_tour.addStep({
    title: 'Einstellungen',
    text: 'Wechseln Sie zu den Einstellungen für Wärme.',
    attachTo: {
        element: '#settings_area_tab',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'settings_area_tab'
});


intro_tour.addStep({
    title: 'Nächster Schritt',
    text: 'Hier gehts weiter zu den Ergebnissen. Im Hintergrund wird dabei automatisch die Simulation Ihres Szenarios gestartet (gelber Kreis rotiert).',
    attachTo: {
        element: '#menu_next_btn',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                document.getElementById("menu_next_btn").click();
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'menu_next_btn2'
});

intro_tour.addStep({
    title: 'Ergebnisse',
    text: 'Sobald die Simulation abgeschlossen ist, können Sie sich die Ergebnisse im Diagramm links und auf der Karte anschauen. Wählen Sie dazu eine Kategorie aus.',
    attachTo: {
        element: '#panel_3_results',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'results_on_map'
});


intro_tour.addStep({
    title: 'Ergebnisse',
    text: 'Wählen Sie auf der Karte eine Region aus und schauen Sie sich die detaillierten Informationen in einem Diagramm an.',
    attachTo: {
        element: '.maplibregl-canvas',
        on: 'top'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'popups'
});


intro_tour.addStep({
    title: 'Einstellungen',
    text: 'Wechseln Sie zwischen der Karten- und der Diagramm-Ansicht, sobald die Simulation abgeschlossen ist.',
    attachTo: {
        element: '#myTab',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                document.getElementById("chart-view-tab").click();
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'chart_view_tab'
});


intro_tour.addStep({
    title: 'Fertig',
    text: 'Viel Spaß mit dem Digiplan-Anhalt-Tool! :D',
    attachTo: {
        element: '#chart_view_tab',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.complete();
            },
            classes: 'shepherd-button-primary',
            text: 'Fertig'
        }
    ],
    id: 'end'
});


//onbaordingCloseBtn.addEventListener("click", function() {
//  intro_tour.start();
//});


const pv_tour = new Shepherd.Tour({  // jshint ignore:line
    useModalOverlay: true,
    defaultStepOptions: {
        cancelIcon: {
            enabled: true
        },
        classes: 'class-1 class-2',
        scrollTo: {behavior: 'smooth', block: 'center'}
    }
});

const pv_more_greatgrandparent = document.querySelector('.c-slider.s_pv_ff_1');
const pv_more_grandparent = pv_more_greatgrandparent.querySelector('.c-slider__label');
const pv_more_parent = pv_more_grandparent.querySelector('.c-slider__label--more');
const pv_more_button = pv_more_parent.querySelector('.button.button--transparent');

pv_tour.addStep({
    title: 'Details',
    text: 'Mehr Details.',
    attachTo: {
        element: pv_more_button,
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.cancel();
            },
            classes: 'shepherd-button-secondary',
            text: 'Tour beenden'
        },
        {
            action() {
                pv_more_button.click();
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'pv_ground_start'
});

pv_tour.addStep({
    title: 'Slider für Agrarflächen geringer Bodengüte',
    text: 'Mehr Details.',
    attachTo: {
        element: '.c-slider.s_pv_ff_3',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'pv_gound_detail1'
});

pv_tour.addStep({
    title: 'Slider für Agri-PV (vertikal)',
    text: 'Mehr Details.',
    attachTo: {
        element: '.c-slider.s_pv_ff_4',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'pv_gound_detail2'
});

pv_tour.addStep({
    title: 'Slider für Agri-PV (hoch aufgeständert)',
    text: 'Mehr Details.',
    attachTo: {
        element: '.c-slider.s_pv_ff_5',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'pv_gound_detail3'
});

pv_tour.addStep({
    title: 'PV Ergebnisse',
    text: 'Mehr Details.',
    attachTo: {
        element: '#pv_ground_key_results',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'pv_gound_detail4'
});

pv_tour.addStep({
    title: 'PV-Freiflächen Slider',
    text: 'So funktioniert der Slider',
    attachTo: {
        element: '.c-slider.s_pv_ff_1',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'pv_ground_slider'
});

pv_tour.addStep({
    title: 'Negativkriterien PV',
    text: 'Bestimmte Negativkriterien auf der Karte ein-/ausschalten',
    attachTo: {
        element: '.map__layers-heading.map__layers-pv',
        on: 'bottom'
    },
    scrollTo: false,
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'pv_ground_criteria'
});

pv_tour.addStep({
    title: 'Naturschutzgebiete',
    text: 'Mit Naturschutzgebieten ausprobieren',
    attachTo: {
        element: '#pv_ground_criteria_nature_monuments',
        on: 'top'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.complete();
            },
            classes: 'shepherd-button-primary',
            text: 'Fertig'
        }
    ],
    id: 'pv_ground_end'
});

const pv_intro_button = document.getElementById('pv_intro_button');
pv_intro_button.addEventListener("click", function() {
    pv_tour.start();
});


const wind_tour = new Shepherd.Tour({  // jshint ignore:line
    useModalOverlay: true,
    defaultStepOptions: {
        cancelIcon: {
            enabled: true
        },
    classes: 'class-1 class-2',
    scrollTo: {behavior: 'smooth', block: 'center'}
}
});

const wind_more_greatgrandparent = document.querySelector('.c-slider.s_w_1');
const wind_more_grandparent = wind_more_greatgrandparent.querySelector('.c-slider__label');
const wind_more_parent = wind_more_grandparent.querySelector('.c-slider__label--more');
const wind_more_button = wind_more_parent.querySelector('.button.button--transparent');

wind_tour.addStep({
    title: 'Details',
    text: 'Mehr Details.',
    attachTo: {
        element: wind_more_button,
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.cancel();
            },
            classes: 'shepherd-button-secondary',
            text: 'Tour beenden'
        },
        {
            action() {
                wind_more_button.click();
                document.getElementById('windPastTab').click();
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'wind_start'
});

wind_tour.addStep({
    title: '2018',
    text: 'Windtab 2018',
    attachTo: {
        element: '#windPastTab',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                document.getElementById('windPresentTab').click();
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'wind_past_tab'
});

wind_tour.addStep({
    title: '2024',
    text: 'Windtab 2024',
    attachTo: {
        element: '#windPresentTab',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'wind_present_tab'
});


wind_tour.addStep({
    title: 'Flächennutzung',
    text: 'Flächennutzung Slider hier',
    attachTo: {
        element: '.c-slider.s_w_6',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                document.getElementById('windFutureTab').click();
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'wind_present_slider'
});


wind_tour.addStep({
    title: '2027',
    text: 'Windtab 2027+',
    attachTo: {
        element: '#windFutureTab',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'wind_future_tab'
});


wind_tour.addStep({
    title: '2027 wind key results',
    text: 'Windtab 2027+',
    attachTo: {
        element: '#wind_key_results_2027',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.next();
            },
            text: 'Weiter'
        }
    ],
    id: 'wind_key_results'
});

wind_tour.addStep({
    title: 'Windernergie Slider',
    text: 'So funktioniert der Slider',
    attachTo: {
        element: '.c-slider.s_w_1',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.back();
            },
            classes: 'shepherd-button-secondary',
            text: 'Zurück'
        },
        {
            action() {
                return this.complete();
            },
            classes: 'shepherd-button-primary',
            text: 'Fertig'
        }
    ],
    id: 'wind_end'
});

const wind_intro_button = document.getElementById('wind_intro_button');
wind_intro_button.addEventListener("click", function() {
    wind_tour.start();
});
