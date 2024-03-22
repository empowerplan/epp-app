"""Add staticfile storage to enable JS module compression."""
from whitenoise.storage import CompressedManifestStaticFilesStorage


class JSModuleCompressedManifestStorage(CompressedManifestStaticFilesStorage):
    """
    Enable JS module support in static files.

    see reference in django docs at
    https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#django.contrib.staticfiles.storage.ManifestStaticFilesStorage
    """

    support_js_module_import_aggregation = True
