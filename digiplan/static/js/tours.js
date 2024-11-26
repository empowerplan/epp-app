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
        // {
        //     action() {
        //         return this.cancel();
        //     },
        //     classes: 'shepherd-button-secondary',
        //     text: 'Tour beenden'
        // },
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
    text: 'Schaue Dir die Situation heute an. Und wähle eine Kategorie aus.',
    attachTo: {
        element: '#situation_today',
        on: 'right'
    },
    buttons: [
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
    text: 'Lasse Dir heutige Anlagen und Flächen auf der Karte anzeigen.',
    attachTo: {
        element: '#js-map-layers-box',
        on: 'top'
    },
    buttons: [
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
    text: 'Klicke auf eine einzelne Windkraftanlage, um mehr über diese zu erfahren.',
    attachTo: {
        element: '.maplibregl-canvas',
        on: 'top'
    },
    buttons: [
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
    text: 'Hier siehst Du ausgewählte Zukunftsszenarien. Wähle eines aus, um es zu erkunden.',
    //Damit werden die Werte in die Einstellungen von Schritt 4 übernommen. Ohne eine Auswahl werden die heutigen Werte eingestellt.
    attachTo: {
        element: '#panel_3_scenarios',
        on: 'right'
    },
    buttons: [
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
    text: 'Hier siehst Du die Rahmenbedingungen für das ausgewählte Szenario.',
    attachTo: {
        element: '#selectedScenario1',
        on: 'left'
    },
    buttons: [
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
    text: 'Bestätige das ausgewählte Szenario hier, um die Einstellungen in den nächsten Schritt zu übernehmen.',
    attachTo: {
        element: '.scenarios__btn',
        on: 'right'
    },
    buttons: [
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
    text: 'Verändere die Einstellungen, um Dein eigenes Szenario zu erstellen.',
    attachTo: {
        element: '#panel_4_settings',
        on: 'right'
    },
    buttons: [
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
    text: 'Hier kannst Du z.B. die Windenergieleistung für Dein Szenario einstellen.<br>Verändere den Hauptregler, um Deine Windleistung anzupassen.',
    attachTo: {
        element: '.s_w_1',
        on: 'right'
    },
    buttons: [
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
    text: 'Hier bei Wind kann die Nutzung der verfügbaren Flächen eingestellt werden.<br><br>Im ersten Schritt kannst Du auswählen, welche Flächenkulisse für Windenergie verwendet werden soll.',
    attachTo: {
        element: '#windTab',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings4'
});


tour.addStep({
    title: 'Detaileinstellungen',
    text: 'Verändere den Regler um zu sehen, wie viel mit Deinen Einstellungen möglich ist.<br><br>Der einstellbare Bereich des linken Hauptreglers passt sich Deinen Einstellungen an.',
    attachTo: {
        element: '.sidepanel',
        on: 'right'
    },
    buttons: [
        {
            action() {
                PubSub.publish(eventTopics.MORE_LABEL_CLICK, document.getElementsByClassName("c-slider s_w_1")[0]);
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings5'
});


tour.addStep({
    title: 'Einstellungen',
    text: 'Den tatsächlichen Wert stellst Du dort anschließend ein.',
    attachTo: {
        element: '.s_w_1',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings6'
});


tour.addStep({
    title: 'Einstellungen',
    text: 'Auch bei der Freiflächen-PV kannst Du Dir die Potenziale ansehen.',
    attachTo: {
        element: '.s_pv_ff_1',
        on: 'right'
    },
    buttons: [
        {
            action() {
                PubSub.publish(eventTopics.MORE_LABEL_CLICK, document.getElementsByClassName("c-slider s_pv_ff_1")[0]);
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings7'
});


tour.addStep({
    title: 'Detaileinstellungen',
    text: 'Du kannst für drei PV-Technologien einstellen, wie viel des Potenzials genutzt werden soll.<br><br>Verändere die Regler um zu sehen, wie viel mit Deinen Einstellungen möglich ist.<br><br>Der einstellbare Bereich des linken Hauptreglers passt sich Deinen Einstellungen an.',
    attachTo: {
        element: '.sidepanel--pv-outdoor',
        on: 'right'
    },
    buttons: [
        {
            action() {
                PubSub.publish(eventTopics.MORE_LABEL_CLICK, document.getElementsByClassName("c-slider s_pv_ff_1")[0]);
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings8'
});


tour.addStep({
    title: 'Einstellungen',
    text: 'Wechsel zu den Einstellungen für Wärme.',
    attachTo: {
        element: '#settings_area_tab',
        on: 'right'
    },
    buttons: [
        {
            action() {
                document.getElementById("heat-tab").click();
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'settings_area_tab'
});


tour.addStep({
    title: 'Einstellungen',
    text: 'Auch für den Wärmesektor kannst Du eigene Einstellungen vornehmen.',
    attachTo: {
        element: '#panel_4_settings',
        on: 'right'
    },
    buttons: [
        {
            action() {
                return this.next();
            },
            classes: 'shepherd-button-primary',
            text: 'Weiter'
        }
    ],
    id: 'panel_4_settings9'
});


tour.addStep({
    title: 'Nächster Schritt',
    text: 'Hier gehts weiter zu den Ergebnissen. Im Hintergrund wird dabei automatisch die Simulation Ihres Szenarios gestartet.',
    attachTo: {
        element: '#menu_next_btn',
        on: 'bottom'
    },
    buttons: [
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
    text: 'Sobald die Simulation abgeschlossen ist, kannst Du die Ergebnisse im Diagramm links und auf der Karte anschauen. Wähle dazu eine Kategorie aus.',
    attachTo: {
        element: '#panel_5_results',
        on: 'right'
    },
    buttons: [
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
    text: 'Wähle auf der Karte eine Region aus und schaue Dir die detaillierten Informationen in einem Diagramm an.',
    attachTo: {
        element: '.maplibregl-canvas',
        on: 'left'
    },
    buttons: [
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
    text: 'Hier kannst Du zwischen der Karten- und der Diagramm-Ansicht wechseln.',
    attachTo: {
        element: '#myTab',
        on: 'bottom'
    },
    buttons: [
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
