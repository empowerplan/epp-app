"""Base settings to build other settings files upon."""
import os

import environ
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_mapengine import setup

ROOT_DIR = environ.Path(__file__) - 3  # (digiplan/config/settings/base.py - 3 = digiplan/)
APPS_DIR = ROOT_DIR.path("digiplan")
DATA_DIR = APPS_DIR.path("data")
METADATA_DIR = APPS_DIR.path("metadata")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = (
    ("en", _("English")),
    ("de", _("German")),
)
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
# 'de' is the standard language
LANGUAGE_CODE = "de"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
if os.environ.get("DATABASE_URL"):
    DATABASES = {"default": env.db("DATABASE_URL")}
else:
    POSTGRES_USER = env.str("POSTGRES_USER")
    POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
    POSTGRES_HOST = env.str("POSTGRES_HOST")
    POSTGRES_PORT = env.str("POSTGRES_PORT")
    POSTGRES_DB = env.str("POSTGRES_DB")
    DATABASE_URL = f"postgis://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    os.environ["DATABASE_URL"] = DATABASE_URL
    DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.forms",
]

THIRD_PARTY_APPS = [
    "foundation_formtags",  # Form layouts
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_distill",
    "django_select2",
]

LOCAL_APPS = ["digiplan.map.apps.MapConfig", "django_oemof", "django_mapengine"]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "digiplan.contrib.sites.migrations"}

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("data"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "digiplan.utils.context_processors.settings_context",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Hendrik Huyskens""", "hendrik.huyskens@rl-institut.de")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s",  # noqa: ISC001
        },
    },
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "root": {"level": "INFO", "handlers": ["console"]},
}


# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# django-libsass
# ------------------------------------------------------------------------------
COMPRESS_PRECOMPILERS = [("text/x-scss", "django_libsass.SassCompiler")]

COMPRESS_CACHEABLE_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# celery
# ------------------------------------------------------------------------------
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Your stuff...
# ------------------------------------------------------------------------------
PASSWORD_PROTECTION = env.bool("PASSWORD_PROTECTION", False)
PASSWORD = env.str("PASSWORD", default=None)
if PASSWORD_PROTECTION and PASSWORD is None:
    msg = "Password protection is on, but no password is given"
    raise ValidationError(msg)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

OEMOF_SCENARIO = env.str("OEMOF_SCENARIO", "scenario_2045")

# django-mapengine
# ------------------------------------------------------------------------------
MAP_ENGINE_CENTER_AT_STARTUP = [12.537917858911896, 51.80812518969171]
MAP_ENGINE_ZOOM_AT_STARTUP = 9
MAP_ENGINE_MAX_BOUNDS = [[11.280733017118229, 51.22918643452503], [13.616574868700604, 52.35515806663738]]

MAP_ENGINE_IMAGES = [
    setup.MapImage("wind", "images/icons/map_wind.png"),
    setup.MapImage("pv", "images/icons/map_pv.png"),
    setup.MapImage("hydro", "images/icons/map_hydro.png"),
    setup.MapImage("biomass", "images/icons/map_biomass.png"),
    setup.MapImage("combustion", "images/icons/map_combustion.png"),
]

MAP_ENGINE_API_MVTS = {
    "municipality": [
        setup.MVTAPI("municipality", "map", "Municipality"),
        setup.MVTAPI("municipalitylabel", "map", "Municipality", "label_tiles"),
    ],
    "results": [setup.MVTAPI("results", "map", "Municipality")],
}

MAP_ENGINE_API_CLUSTERS = [
    setup.ClusterAPI("wind", "map", "WindTurbine"),
    setup.ClusterAPI("pvroof", "map", "PVroof"),
    setup.ClusterAPI("pvground", "map", "PVground"),
    setup.ClusterAPI("hydro", "map", "Hydro"),
    setup.ClusterAPI("biomass", "map", "Biomass"),
    setup.ClusterAPI("combustion", "map", "Combustion"),
]

MAP_ENGINE_STYLES_FOLDER = "digiplan/static/config/"
MAP_ENGINE_ZOOM_LEVELS = {
    "municipality": setup.Zoom(8, 12),
}

MAP_ENGINE_CHOROPLETHS = [
    setup.Choropleth("population", layers=["municipality"], title=_("Einwohner_innenzahl"), unit=_("EW")),
    setup.Choropleth("population_density", layers=["municipality"], title=_("Einwohner_innenzahl"), unit=_("EW/qm")),
    setup.Choropleth("capacity", layers=["municipality"], title=_("Installierte Leistung"), unit=_("MW")),
    setup.Choropleth(
        "capacity_square",
        layers=["municipality"],
        title=_("Installierte Leistung pro qm"),
        unit=_("MW/qm"),
    ),
    setup.Choropleth("wind_turbines", layers=["municipality"], title=_("Anzahl Windturbinen"), unit=_("")),
    setup.Choropleth(
        "wind_turbines_square",
        layers=["municipality"],
        title=_("Anzahl Windturbinen pro qm"),
        unit=_(""),
    ),
    setup.Choropleth(
        "renewable_electricity_production",
        layers=["municipality"],
        title=_("Energie Erneuerbare"),
        unit=_("GWh"),
    ),
]

MAP_ENGINE_POPUPS = [
    setup.Popup(
        "municipality",
        popup_at_default_layer=False,
        choropleths=[
            "population",
            "population_density",
            "capacity",
            "capacity_square",
            "wind_turbines",
            "wind_turbines_square",
            "renewable_electricity_production",
        ],
    ),
]
