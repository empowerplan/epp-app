# Verwendete Technologien

## Kartendarstellung

Für die Kartendarstellung wird [Maplibre GL JS](https://maplibre.org/maplibre-gl-js/docs/) im Frontend verwendet.
Die Bibliothek ermöglicht das Darstellen von Kartenlayern aus einer Vector Tiles Quelle sowie aus einer GeoJSON.
Die Daten für die Karte werden vorab als Geopackages bereitgestellt (siehe [Datenstruktur](data_structure.md)) und 
in die Geo-Datenbank (PostGis) geladen. 
Von dort werden die Kartenlayer mithilfe der am RLI entwickelten Bibliothek [`django-mapengine`](https://github.com/rl-institut/django-mapengine) aufbereitet und der Applikation zur Verfügung gestellt.
Im Falle von Polygonen können mehrere Layer gebündelt als Multi-Vector-Tiles (MVTs) unter einer URL bereitgestellt werden (https://maplibre.org/maplibre-gl-js/docs/API/classes/VectorTileSource/).
Sollen Daten (zum Beispiel Erzeugungsanlagen) auf der Karte je nach Zoomstufe als Punkte oder geclustert dargestellt werden, benötigt maplibre-gl-js diese Daten in Form von GeoJSONs (https://maplibre.org/maplibre-gl-js/docs/API/classes/GeoJSONSource/).
In diesem Falle stellt `django-mapengine` die benötigten Daten als GeoJSONs per URL-Schnittstelle zur Verfügung.

In der Karte können außerdem [Choropleths](https://de.wikipedia.org/wiki/Choroplethenkarte) oder Popups angezeigt werden.
`django-mapengine` holt sich die dafür benötigten Daten von einer vordefinierten Schnittstelle (URL) des Programms.


## Energiesystemoptimierung

Für die Energiesystemoptimierung wird [oemof-solph](https://github.com/oemof/oemof-solph) verwendet. 
Die Daten liegen vorab als CSVs bereit und werden mittels [oemof-tabular](https://github.com/oemof/oemof-tabular) eingelesen. 
Die Integration in die Django-Anwendung erfolgt mithilfe von [django-oemof](https://github.com/rl-institut/django-oemof), 
welches die Schnittstelle zwischen der Webapplikation und dem Energiesystemmodell bereitstellt. 
Die Benutzereingaben aus der Weboberfläche werden über Hooks verarbeitet, die in der Datei `hooks.py` implementiert sind. 
Diese Hooks passen die Parameter des Energiesystemmodells entsprechend der Benutzereingaben an, bevor die Optimierung durchgeführt wird. 
Zur Reduzierung der Rechenzeit wurde [TSAM (Time Series Aggregation Module)](https://github.com/FZJ-IEK3-VSA/tsam) eingesetzt, 
um die zeitliche Auflösung der Eingangsdaten zu verringern, indem repräsentative Zeitperioden identifiziert werden.
