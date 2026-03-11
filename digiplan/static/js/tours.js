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
  title: 'Freiflächen-Photovoltaik',
  text:
      'Erfahre mehr über verfügbare Flächen für PV in der Region und lege ' +
      'fest, wie viel davon genutzt werden sollen.' +
      '<br><b>Klappe dafür das Detailmenü auf.</b>',
  attachTo: {
    element: pv_more_button,
    on: 'bottom'
  },
  buttons: [
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
  title: 'Freiflächen-PV',
  text:
      'Es stehen mehrere PV-Arten zur Verfügung:' +
      '<br><br>' +
      '<div style="display:flex;align-items:flex-start;gap:0.6rem;margin-bottom:0.6rem">' +
        '<svg width="40" height="40" viewBox="0 0 48 48.01" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">' +
          '<path fill="#F8D637" d="M34.71,42.11v-7.61h8.56l-9.73-30.33H13.6l-9.27,30.33h8.43v7.61H1.9v2h44.19v-2h-11.38Z' +
          'M25,32.5v-7.77h13.02l2.49,7.77h-15.52ZM25,15.28h9.99l2.39,7.45h-12.38v-7.45Z' +
          'M23,22.73h-12.99l2.28-7.45h10.71v7.45ZM34.36,13.28h-9.35v-7.11h7.07l2.28,7.11Z' +
          'M15.08,6.17h7.92v7.11h-10.1l2.17-7.11ZM9.41,24.73h13.6v7.77H7.04l2.37-7.77Z' +
          'M14.76,34.5h17.94v7.61H14.76v-7.61Z"/>' +
        '</svg>' +
        '<div><b>"Klassische" Freiflächen-PV:</b> Module in Reihen niedrig aufgeständert, auf Flächen mit geringer Bodengüte.</div>' +
      '</div>' +
      '<div style="display:flex;align-items:flex-start;gap:0.6rem;margin-bottom:0.6rem">' +
        '<svg width="40" height="40" viewBox="0 0 48 48.01" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">' +
          '<path fill="#c19800" d="M21.54,2.43H7.83L1.82,36.05h5.46v9.73h2v-9.73h11.01v9.73h2v-9.73h5.55L21.54,2.43Z' +
          'M15.97,14.22h5.75l1.39,7.41h-7.14v-7.41ZM13.97,21.63h-7.54l1.32-7.41h6.22v7.41Z' +
          'M23.48,23.63l1.95,10.42h-9.46v-10.42h7.51ZM21.34,12.22h-5.37v-7.79h3.91l1.46,7.79Z' +
          'M13.97,4.43v7.79h-5.86l1.39-7.79h4.47ZM6.07,23.63h7.9v10.42H4.21l1.86-10.42Z"/>' +
          '<path fill="#c19800" d="M46.26,27.98l-.06-.74-.72-.16c-.14-.03-3.35-.7-5.6,1.16v-2.84c1.22-.01,3.1-.28,4.53-1.59,' +
          '1.4-1.29,2-3.25,1.8-5.8l-.06-.74-.72-.16c-.09-.02-1.57-.33-3.22.03.14-.41.24-.84.27-1.3.13-1.95-.86-3.85-2.95-5.64l-.6-.51-.64.46' +
          'c-.12.08-2.87,2.1-2.99,5.14-.03.64.08,1.28.28,1.9-.92-.25-1.97-.34-3.15-.24l-.74.06-.16.72c-.03.14-.73,3.44,1.24,5.7,' +
          '1.12,1.29,2.83,1.94,5.08,1.94,0,0,.01,0,.02,0v2.95c-1.28-1.11-3.08-1.58-5.38-1.4l-.74.06-.16.72c-.03.14-.73,3.44,1.24,5.7,' +
          '1.12,1.28,2.81,1.93,5.04,1.94v10.54h2v-10.51c1.22,0,3.14-.26,4.59-1.59,1.4-1.29,2-3.25,1.8-5.8Z' +
          'M44.24,18.98c0,1.5-.4,2.63-1.19,3.36-.95.88-2.3,1.06-3.18,1.07v-.02h-.05c0-.16,0-.32-.01-.5.09-1.36.48-2.38,1.21-3.02.98-.85,2.36-.94,3.21-.89Z' +
          'M38.86,12.3c1.15,1.15,1.7,2.29,1.62,3.39-.08,1.29-1.01,2.33-1.65,2.9-1.06-1.06-1.57-2.14-1.54-3.21.05-1.33.94-2.45,1.56-3.07Z' +
          'M33.41,18.9c1.5,0,2.63.4,3.36,1.19.74.79.98,1.87,1.05,2.72-.01.18-.02.36-.02.55-1.6-.01-2.78-.43-3.49-1.24-.85-.98-.93-2.37-.89-3.21Z' +
          'M33.46,28.87c1.5,0,2.63.4,3.36,1.19.74.79.98,1.87,1.05,2.72-.01.18-.02.36-.02.55-1.6-.01-2.78-.43-3.49-1.24-.85-.98-.93-2.37-.89-3.21Z' +
          'M43.12,32.3c-.96.89-2.34,1.06-3.23,1.07,0-.16,0-.33-.01-.52.09-1.35.48-2.38,1.21-3.02.98-.86,2.37-.94,3.21-.89,0,1.5-.4,2.63-1.19,3.36Z"/>' +
        '</svg>' +
        '<div><b>Agri-PV auf Agrarflächen:</b> Vertikale Module in Reihen, gemeinsame Nutzung mit der Landwirtschaft.</div>' +
      '</div>' +
      '<div style="display:flex;align-items:flex-start;gap:0.6rem;margin-bottom:0.75rem">' +
        '<svg width="40" height="40" viewBox="0 0 48 48.01" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">' +
          '<path fill="#5F4F03" d="M46.88,1.67h-30.83L1.04,19.58h4.44v27.24h2v-27.24h26.93l6.69-9.6v37.01h2V7.1l3.79-5.43Z' +
          'M43.05,3.67l-4.12,5.91h-12.9l4.13-5.91h12.89ZM16.98,3.67h10.74l-4.13,5.91h-11.57l4.96-5.91Z' +
          'M10.35,11.58h11.84l-4.19,6H5.32l5.03-6ZM33.36,17.58h-12.92l4.19-6h12.9l-4.18,6Z"/>' +
          '<path fill="#5F4F03" d="M31.43,35.91l-.72-.16c-.14-.03-3.29-.69-5.54,1.12v-2.9c.87-.71,2.45-2.29,2.6-4.49,' +
          '.14-1.95-.86-3.85-2.95-5.64l-.6-.51-.64.46c-.12.08-2.87,2.1-2.99,5.14-.07,1.81.8,3.54,2.58,5.14v2.97' +
          'c-1.29-1.15-3.11-1.64-5.44-1.46l-.74.06-.16.72c-.03.14-.73,3.44,1.24,5.7,1.12,1.29,2.83,1.94,5.08,1.94,0,0,.02,0,.02,0v2.67h2v-2.63' +
          'c1.22-.01,3.1-.27,4.53-1.59,1.4-1.29,2-3.25,1.8-5.8l-.06-.74Z' +
          'M22.59,29.02c.05-1.33.94-2.45,1.56-3.07,1.15,1.15,1.69,2.29,1.62,3.39-.09,1.29-1,2.32-1.64,2.89h-.02c-1.05-1.06-1.57-2.14-1.53-3.21Z' +
          'M18.7,37.54c1.5,0,2.63.4,3.36,1.19.74.79.98,1.87,1.05,2.72-.01.18-.02.36-.02.55-1.6-.01-2.78-.43-3.49-1.24-.85-.98-.93-2.37-.89-3.21Z' +
          'M28.35,40.97c-.95.88-2.3,1.06-3.18,1.07v-1.2c.16-1.02.55-1.81,1.15-2.34.98-.85,2.37-.93,3.21-.89,0,1.5-.4,2.63-1.19,3.36Z"/>' +
        '</svg>' +
        '<div><b>Agri-PV über Dauerkulturen:</b> Module überdachen z.B. Obstplantagen teilweise.</div>' +
      '</div>' +
      '<b>Verschiebe die Regler, um den zu nutzenden Flächenanteil ' +
      'festzulegen.</b>' +
      '<br><br><b>Unten</b> siehst Du, wie viel Fläche benötigt und Energie ' +
      'erzeugt wird.' +
      '<br><b>Links</b> siehst Du, wie sich die installierbare Leistung ' +
      'verändert. Die Markierungen <b>BB30</b> und <b>BB40</b> zeigen die ' +
      'Zielwerte für 2030 und 2040, abgeleitet aus der Energiestrategie ' +
      'Brandenburg für die Region.',
  attachTo: {
    element: '.sidepanel.sidepanel--pv-outdoor',
    on: 'right'
  },
  buttons: [
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
  title: 'Regionale Potenzialflächen',
  text: 'Klicke auf eine Gemeinde, um deren PV-Potentialflächen zu erkunden.',
  attachTo: {
    element: '#map',
    on: 'top'
  },
  canClickTarget: true,
  buttons: [
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

// pv_tour.addStep({
//   title: 'PV-Freiflächen Slider',
//   text: 'Hier kannst Du nun einstellen, wie viel Leistung installiert werden soll.',
//   attachTo: {
//     element: '.c-slider.s_pv_ff_1',
//     on: 'right'
//   },
//   buttons: [
//     {
//       action() {
//         return this.next();
//       },
//       text: 'Weiter'
//     }
//   ],
//   id: 'pv_ground_slider'
// });

pv_tour.addStep({
  title: 'Negativkriterien PV',
  text:
      'Aber nicht alle Flächen stehen auch zur Verfügung:' +
      '<br><br>' +
      'Es gibt sog. Negativkriterien. Dazu zählen etwa sensible Natur- oder ' +
      'Schutzräume (z.B. Naturschutzgebiete), in denen PV‑Freiflächenanlagen ' +
      'nicht genehmigungsfähig sind.' +
      '<br><br>' +
      '<b>Hier kannst Du Negativkriterien auf der Karte ein-/ausschalten ' +
      'und prüfen, welche Potenzialflächen tatsächlich infrage kommen.</b>',
  attachTo: {
    element: '.map__layers-heading.map__layers-pv',
    on: 'bottom'
  },
  scrollTo: false,
  buttons: [
    {
      action() {
        // Activate layer
        document.querySelector(".static-layer #priority_climate_resistent_agri_distilled").click();
        // Fly and zoom
        map.flyTo({
            center: [13.84, 52.73],
            zoom: 11,
            essential: true
        });
        return this.next();
      },
      text: 'Weiter'
    }
  ],
  id: 'pv_ground_criteria'
});

pv_tour.addStep({
  title: 'Naturschutzgebiete',
  text:
      'In dieser Gemeinde gibt es z.B. Vorzugsgebiete für klimarobustes ' +
      'Ackerland, die für Freiflächen-PV nicht zur Verfügung stehen.',
  attachTo: {
    element: '#priority_climate_resistent_agri,#priority_climate_resistent_agri_distilled',
    on: 'top-end'
  },
  canClickTarget: true,
  buttons: [
    {
      action() {
        // Deactivate layer
        document.querySelector(".static-layer #priority_climate_resistent_agri_distilled").click();
        // Reset zoom
        map.zoomTo(8);
        return this.next();
      },
      classes: 'shepherd-button-primary',
      text: 'Weiter'
    }
  ],
  id: 'pv_ground_layer'
});

pv_tour.addStep({
  title: 'Selbst ausprobieren',
  text:
      'Du kennst jetzt die wichtigsten Funktionen für Freiflächen-PV.' +
      '<br><br>' +
      'Stelle die Regler nach Deinen Vorstellungen ein: Welche Flächen sollen ' +
      'genutzt werden – und wie viel Leistung ist damit installierbar?' +
      '<br><br>' +
      'Die Ergebnisse siehst Du direkt in den Zahlen und auf der Karte.',
  attachTo: {
    element: '.sidepanel.sidepanel--pv-outdoor',
    on: 'right'
  },
  buttons: [
    {
      action() {
        return this.complete();
      },
      classes: 'shepherd-button-primary',
      text: 'Los geht\'s'
    }
  ],
  id: 'pv_ground_cta'
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
  title: 'Windflächen erkunden',
  text:
      'Erfahre mehr über verfügbare Flächen für Windenergie in der Region und ' +
      'lege fest, wie viel davon genutzt werden sollen.' +
      '<br><b>Klappe dafür das Detailmenü auf.</b>',
  attachTo: {
    element: wind_more_button,
    on: 'bottom'
  },
  buttons: [
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
  title: 'Regionalplan 2018',
  text:
      'Der <b>Sachliche Teilregionalplan Windenergie 2018</b> hat ' +
      'Vorranggebiete für Windenergie in der Region Oderland-Spree festgelegt.' +
      '<br><br>' +
      'Diese Flächen waren die Grundlage für Genehmigungsverfahren bis zur ' +
      'Ablösung durch den neuen Regionalplan.' +
      '<br><br>' +
      '<b>Unten</b> siehst Du, wie viel Fläche, wie viele Anlagen und wie viel ' +
      'Energie auf diesen Flächen möglich wären.',
  attachTo: {
    element: '#windPastTab',
    on: 'bottom'
  },
  buttons: [
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
  title: 'Regionalplan 2024',
  text:
      'Der Sachliche Teilregionalplan Erneuerbare Energien 2024 legt einen ' +
      'Entwurf neuer Vorranggebiete für Windenergie fest.' +
      '<br><br>' +
      'Grundlage ist das Windenergieflächenbedarfsgesetz (WindBG), das ' +
      'Brandenburg verpflichtet, bis 2027 mindestens 1,8 % der Landesfläche ' +
      'für Windenergie auszuweisen.',
  attachTo: {
    element: '#windPresentTab',
    on: 'bottom'
  },
  buttons: [
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
  title: 'Flächennutzung 2024',
  text:
      'Mit diesem <b>Regler</b> stellst Du ein, welcher Anteil der dargestellten ' +
      'Vorranggebiete 2024 für Windenergie genutzt werden sollen.' +
      '<br><br>' +
      '<b>Unten</b> siehst Du, wie viel Fläche, wie viele Anlagen und wie viel ' +
      'Energie damit möglich sind.' +
      '<br><b>Links</b> siehst Du, wie sich die installierbare Leistung verändert.',
  attachTo: {
    element: '.c-slider.s_w_6',
    on: 'right'
  },
  buttons: [
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
  title: 'Flächennutzung 2027+',
  text:
      'Über die Vorranggebiete 2024 hinaus gibt es weitere potenzielle ' +
      'Flächen für Windenergie nach 2027 (schraffiert).' +
      '<br><br>' +
      'Grundlage ist das Windenergieflächenbedarfsgesetz (WindBG), das ' +
      'Brandenburg verpflichtet, bis 2032 mindestens 2,2 % der Landesfläche ' +
      'für Windenergie auszuweisen.' +
      '<br>Dies können insbesondere kommunale Planungen außerhalb der ' +
      'Vorranggebiete sein, die einen Beitrag zur Flächenzielerreichung ' +
      'leisten.' +
      '<br><br>' +
      '<b>Verschiebe den Regler</b>, um den Anteil der Gebiete festzulegen, ' +
      'der in Deinem Szenario erschlossen werden soll.',
  attachTo: {
    element: '#windFutureTab',
    on: 'right'
  },
  buttons: [
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
  title: 'Potenzial 2027+',
  text:
      'Hier siehst Du das Ergebnis Deiner Einstellungen für die Suchräume 2027+:' +
      '<br><ul>' +
      '<li>Wie viel <b>Fläche</b> genutzt werden könnte</li>' +
      '<li>Wie viele <b>Anlagen</b> errichtet werden könnten</li>' +
      '<li>Wie viel <b>Energie</b> erzeugt werden könnte</li>' +
      '</ul>' +
      'Die Werte für alle drei Flächenkulissen zusammen bestimmen den ' +
      'maximalen Rahmen für den Hauptregler links.',
  attachTo: {
    element: '#wind_key_results_2027',
    on: 'right'
  },
  buttons: [
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
  text: 'Klicke auf eine Gemeinde, um deren Windpotenzialflächen auf der Karte zu erkunden.',
  attachTo: {
    element: '#map',
    on: 'top'
  },
  canClickTarget: true,
  buttons: [
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
  title: 'Leistung einstellen',
  text:
      'Den tatsächlichen Wert der <b>installierten Windleistung</b> stellst ' +
      'Du mit diesem Hauptregler ein.' +
      '<br><br>' +
      'Der einstellbare Bereich passt sich automatisch an Deine ' +
      'Flächeneinstellungen an - auf mehr Fläche kannst Du mehr Leistung ' +
      'installieren.' +
      '<br><br>' +
      'Die Markierungen <b>BB30</b> und <b>BB40</b> zeigen die Zielwerte ' +
      'für 2030 und 2040, abgeleitet aus der Energiestrategie Brandenburg ' +
      'für die Region.',
  attachTo: {
    element: '.c-slider.s_w_1',
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
  id: 'wind_end'
});

wind_tour.addStep({
  title: 'Selbst ausprobieren',
  text:
      'Du kennst jetzt die wichtigsten Funktionen für Windenergie.' +
      '<br><br>' +
      'Stelle die Regler nach Deinen Vorstellungen ein: Welche Flächenkulisse ' +
      'soll genutzt werden – und wie viel Leistung ist damit installierbar?' +
      '<br><br>' +
      'Die Ergebnisse siehst Du direkt in den Zahlen und auf der Karte.',
  attachTo: {
    element: '.sidepanel.sidepanel--wind',
    on: 'right'
  },
  buttons: [
    {
      action() {
        return this.complete();
      },
      classes: 'shepherd-button-primary',
      text: 'Los geht\'s'
    }
  ],
  id: 'wind_cta'
});

const wind_intro_button = document.getElementById('wind_intro_button');
wind_intro_button.addEventListener("click", function () {
  wind_tour.start();
});
