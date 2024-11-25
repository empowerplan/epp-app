const intro_start_button = document.getElementById("intro_tour_start");

const tour = new Shepherd.Tour({  // jshint ignore:line
    useModalOverlay: true,
    defaultStepOptions: {
        cancelIcon: {
            enabled: true
        },
        classes: 'class-1 class-2',
        scrollTo: {behavior: 'smooth', block: 'center'}
    }
});


tour.addStep({
    title: 'Navigation',
    text: 'Schritt für Schritt zu Ihrem eigenen Szenario.',
    attachTo: {
        element: '.wizard__main',
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
                const menu_next_btn = document.getElementById("menu_next_btn");
                menu_next_btn.click();
                // document.getElementById("menu_next_btn").click();
                // document.getElementById("menu_next_btn").click();
                return this.next();
            },
            text: 'Weiter'
        }

    ],
    id: 'start'
});

tour.addStep({
    title: 'Situation heute',
    text: 'Schauen Sie sich die Situation heute an. Und wählen sie eine Kategorie aus.',
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
                // Show choropleth
                const statusquoDropdown = document.getElementById("situation_today");
                statusquoDropdown.value = "energy_statusquo";
                PubSub.publish(mapEvent.CHOROPLETH_SELECTED, statusquoDropdown.value);
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'situation_today'
});


tour.addStep({
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
                document.querySelector(".static-layer #rpg_ols_wind_operating").click();
                document.querySelector(".static-layer #special_protection_area").click();
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'region_chart'
});


tour.addStep({
    title: 'Karte',
    text: 'Lassen Sie sich heutige Anlagen und Flächen auf der Karte anzeigen.',
    attachTo: {
        element: '#js-map-layers-box',
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
                // Deactivate layer
                document.querySelector(".static-layer #special_protection_area").click();
                // Fly to wind turbine
                map.flyTo({
                  center: [14.195, 52.425],
                  zoom: 14,
                  essential: true
                });
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'layer_switch'
});


tour.addStep({
    title: 'Karte',
    text: 'Klicken Sie auf eine einzelne Windkraftanlage, um mehr über diese zu erfahren.',
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
                // Deactivate layer
                document.querySelector(".static-layer #rpg_ols_wind_operating").click();
                map.zoomTo(8);
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'cluster_popup'
});


tour.addStep({
    title: 'Nächster Schritt',
    text: 'Hier gehts weiter zu den Szenarien.',
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
    id: 'menu_next_btn1'
});


tour.addStep({
    title: 'Szenarien',
    text: 'Hier sehen Sie ausgewählte Zukunftsszenarien. Wählen Sie eines aus, um es zu erkunden.',
    //Damit werden die Werte in die Einstellungen von Schritt 4 übernommen. Ohne eine Auswahl werden die heutigen Werte eingestellt.
    attachTo: {
        element: '#panel_3_scenarios',
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
    id: 'panel_3_scenarios'
});


tour.addStep({
    title: 'Szenarien',
    text: 'Hier sehen Sie die Rahmenbedingungen für das ausgewählte Szenario.',
    attachTo: {
        element: '#selectedScenario1',
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
    id: 'panel_3_scenarios2'
});


tour.addStep({
    title: 'Szenarien',
    text: 'Bestätigen Sie das ausgewählte Szenario hier, dann werden die Einstellungen in den nächsten Schritt übernommen.',
    attachTo: {
        element: '.scenarios__btn',
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
    id: 'panel_3_scenarios3'
});


tour.addStep({
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
    id: 'menu_next_btn2'
});


tour.addStep({
    title: 'Einstellungen',
    text: 'Verändern Sie die Einstellungen, um Ihr eigenes Szenario zu erstellen.',
    attachTo: {
        element: '#panel_4_settings',
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
    id: 'panel_4_settings1'
});

tour.addStep({
    title: 'Einstellungen',
    text: 'Beispiel: Hier können Sie die Windenergieleistung einstellen.',
    attachTo: {
        element: '.s_w_1',
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
    id: 'panel_4_settings2'
});


tour.addStep({
    title: 'Detaileinstellungen',
    text: 'Für einige Erzeuger gibt es Detaileinstellungen.',
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
                PubSub.publish(eventTopics.MORE_LABEL_CLICK, document.getElementsByClassName("c-slider s_w_1")[0]);
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings3'
});


tour.addStep({
    title: 'Detaileinstellungen',
    text: 'Hier bei Wind können die verfügbaren Flächen eingestellt werden.',
    attachTo: {
        element: '.sidepanel',
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
                PubSub.publish(eventTopics.MORE_LABEL_CLICK, document.getElementsByClassName("c-slider s_w_1")[0]);
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings4'
});


tour.addStep({
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


tour.addStep({
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
    id: 'menu_next_btn3'
});

tour.addStep({
    title: 'Ergebnisse',
    text: 'Sobald die Simulation abgeschlossen ist, können Sie sich die Ergebnisse im Diagramm links und auf der Karte anschauen. Wählen Sie dazu eine Kategorie aus.',
    attachTo: {
        element: '#panel_5_results',
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


tour.addStep({
    title: 'Ergebnisse',
    text: 'Wählen Sie auf der Karte eine Region aus und schauen Sie sich die detaillierten Informationen in einem Diagramm an.',
    attachTo: {
        element: '.maplibregl-canvas',
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
    id: 'popups'
});


tour.addStep({
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


tour.addStep({
    title: 'Fertig',
    text: 'Viel Spaß mit dem EmPowerPlan-Tool! :D',
    attachTo: null,
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


intro_start_button.addEventListener("click", function() {
  tour.start();
});
