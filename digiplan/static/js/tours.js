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
    text: 'Schritt für Schritt zu Deinem eigenen Szenario.',
    attachTo: {
        element: '.wizard__main',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                const menu_next_btn = document.getElementById("menu_next_btn");
                menu_next_btn.click();
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
                document.querySelector(".static-layer #special_protection_area_distilled").click();
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
                document.querySelector(".static-layer #special_protection_area_distilled").click();
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
    text: 'Hier gehts weiter zu den Ergebnissen. Im Hintergrund wird dabei automatisch die Simulation Deines Szenarios gestartet.',
    attachTo: {
        element: '#menu_next_btn',
        on: 'bottom'
    },
    buttons: [
        {
            action() {
                document.getElementById("wind-tab").click();
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
    text: 'Die Simulation kann einen Moment dauern, anschließend kannst Du die Ergebnisse im Diagramm links und auf der Karte anschauen.<br><br>Derweil kannst Du Dir schon einige Vorergebnisse ansehen.',
    attachTo: {
        element: '#panel_5_results',
        on: 'right'
    },
    buttons: [
        {
            action() {
                // Show choropleth
                const futureDropdown = document.getElementById("result_views");
                futureDropdown.value = "energy_2045";
                PubSub.publish(mapEvent.CHOROPLETH_SELECTED, futureDropdown.value);
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
    text: 'Wähle auf der Karte eine Gemeinde aus und schaue Dir die Details in einem Diagramm an.',
    attachTo: {
        element: '.maplibregl-canvas',
        on: 'left'
    },
    buttons: [
        {
            action() {
                // Hide status quo choropleth again
                const futureDropdown = document.getElementById("result_views");
                futureDropdown.value = "";
                deactivateChoropleth();
                PubSub.publish(eventTopics.CHOROPLETH_DEACTIVATED);
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
    id: 'chart_view_tab1'
});

tour.addStep({
    title: 'Einstellungen',
    text: 'Wähle eine Ergebnis-Kategorie',
    attachTo: {
        element: '.nav-pills',
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
    id: 'chart_view_tab2'
});


tour.addStep({
    title: 'Einstellungen',
    text: 'Wie viel trägt der ausgewählte Energieträger zur Deckung des Strombedarfs bei?',
    attachTo: {
        element: '#mainTabContent',
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
    id: 'chart_view_tab3'
});


tour.addStep({
    title: 'Fertig',
    text: 'Viel Spaß mit dem EmPowerPlan-Tool!',
    attachTo: null,
    buttons: [
        {
            action() {
                document.getElementById("menu_previous_btn").click();
                document.getElementById("menu_previous_btn").click();
                document.getElementById("menu_previous_btn").click();
                document.getElementById("menu_previous_btn").click();
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
  title: 'Regionale Potenzialflächen',
  text: 'Klicken Sie auf eine Gemeinde, um deren PV-Potentialflächen zu erkunden.',
  attachTo: {
    element: '#map',
    on: 'top'
  },
  canClickTarget: true,
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
  id: 'pv_ground_region'
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
    element: '#pv_ground_criteria_nature_monuments,#pv_ground_criteria_nature_monuments_distilled',
    on: 'top-end'
  },
  canClickTarget: true,
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
pv_intro_button.addEventListener("click", function () {
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
  title: 'Regionale Potenzialflächen',
  text: 'Klicken Sie auf eine Gemeinde, um deren Wind-Potentialflächen zu erkunden.',
  attachTo: {
    element: '#map',
    on: 'top'
  },
  canClickTarget: true,
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
  id: 'wind_region'
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
wind_intro_button.addEventListener("click", function () {
  wind_tour.start();
});
