from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import (
    UserMeasurementViewSet,
    LocationViewSet,
    DeviceViewSet,
    ProbeViewSet,
    MeasurementViewSet
)


router = routers.DefaultRouter()
router.register("data-log", UserMeasurementViewSet, basename="User")
router.register("locations", LocationViewSet, basename="Location")
router.register("devices", DeviceViewSet, basename="Device")
router.register("probes", ProbeViewSet, basename="Probe")
router.register("measurements", MeasurementViewSet, basename="Measurement")

urlpatterns = [
    path("", include(router.urls)),
]
