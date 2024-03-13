"""Admin model to register django models in admin interface."""
from django.contrib import admin

from .models import PVGroundCriteriaAviation

admin.site.register(PVGroundCriteriaAviation)
