import json
import pathlib
from collections import namedtuple

from django.conf import settings
from range_key_dict import RangeKeyDict

from digiplan import __version__
from digiplan.map import utils

# FILES

STYLES_DIR = settings.APPS_DIR.path("static").path("styles")

CLUSTER_GEOJSON_FILE = settings.DATA_DIR.path("cluster.geojson")
LAYER_STYLES_FILE = STYLES_DIR.path("layer_styles.json")
RESULT_STYLES_FILE = STYLES_DIR.path("result_styles.json")
CHOROPLETH_STYLES_FILE = STYLES_DIR.path("choropleth_styles.json")
PARAMETERS_FILE = pathlib.Path(__file__).parent / "parameters.json"

# REGIONS

MIN_ZOOM = 6
MAX_ZOOM = 22
MAX_DISTILLED_ZOOM = 10

Zoom = namedtuple("MinMax", ["min", "max"])
ZOOM_LEVELS = {
    "municipality": Zoom(8, MAX_ZOOM),
}
REGIONS = ("municipality",)
REGION_ZOOMS = RangeKeyDict({zoom: layer for layer, zoom in ZOOM_LEVELS.items() if layer in REGIONS})


# FILTERS

FILTER_DEFINITION = {}
REGION_FILTER_LAYERS = ["built_up_areas", "settlements", "hospitals"]


# PARAMETERS

with open(PARAMETERS_FILE, "r", encoding="utf-8") as param_file:
    PARAMETERS = json.load(param_file)


# STORE

STORE_COLD_INIT = {
    "version": __version__,
    "debugMode": settings.DEBUG,
    "zoom_levels": ZOOM_LEVELS,
    "region_filter_layers": REGION_FILTER_LAYERS,
    "slider_marks": {
        param_name: [("Status Quo", param_data["status_quo"])]
        for param_name, param_data in PARAMETERS.items()
        if "status_quo" in param_data
    },
}


def init_hot_store():
    # Filter booleans have to be stored as str:
    filter_init = {data["js_event_name"]: "True" if data["initial"] else "False" for data in FILTER_DEFINITION.values()}
    return json.dumps(filter_init)


STORE_HOT_INIT = init_hot_store()


# SOURCES


def init_sources():
    sources = {}
    metadata_path = pathlib.Path(settings.METADATA_DIR)
    for metafile in metadata_path.iterdir():
        if metafile.suffix != ".json":
            continue
        with open(metafile, "r", encoding="utf-8") as metadata_raw:
            metadata = json.loads(metadata_raw.read())
            sources[metadata["id"]] = metadata
    return sources


SOURCES = init_sources()


# STYLES

RESULTS_CHOROPLETHS = utils.Choropleth(RESULT_STYLES_FILE)
STATIC_CHOROPLETHS = utils.Choropleth(CHOROPLETH_STYLES_FILE)

with open(LAYER_STYLES_FILE, mode="r", encoding="utf-8") as layer_styles_file:
    LAYER_STYLES = json.load(layer_styles_file)
LAYER_STYLES.update(STATIC_CHOROPLETHS.get_all_styles())


# MAP
MapImage = namedtuple("MapImage", ["name", "path"])
MAP_IMAGES = [MapImage("hospital", "images/icons/hospital.png")]


# DISTILL

# Tiles of Ghana: At z=5 Ghana has width x=15-16 and height y=15(-16)
X_AT_MIN_Z = 31
Y_AT_MIN_Z = 30
X_OFFSET = 1
Y_OFFSET = 1


def get_tile_coordinates_for_region(region):
    for z in range(MIN_ZOOM, MAX_DISTILLED_ZOOM + 1):
        z_factor = 2 ** (z - MIN_ZOOM)
        for x in range(X_AT_MIN_Z * z_factor, (X_AT_MIN_Z + 1) * z_factor + X_OFFSET):
            for y in range(Y_AT_MIN_Z * z_factor, (Y_AT_MIN_Z + 1) * z_factor + Y_OFFSET):
                if region in REGIONS and REGION_ZOOMS[z] != region:
                    continue
                yield x, y, z
