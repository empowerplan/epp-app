"""URLs for map app, including main view and API points."""


from django.urls import path

from . import views

app_name = "map"

urlpatterns = [
    path("", views.MapGLView.as_view(), name="map"),
    path("choropleth/<str:lookup>/<str:layer_id>", views.get_choropleth, name="choropleth"),
    path("popup/<str:lookup>/<int:region>", views.get_popup, name="popup"),
    path("charts", views.get_charts, name="charts"),
    path("pre_result", views.store_pre_result, name="pre_result"),
]
