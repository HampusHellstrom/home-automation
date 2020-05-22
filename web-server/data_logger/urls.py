from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import (
    UserMeasurementViewSet,
    SensorViewSet,
    MeasurementViewSet,
    SensorGroupViewSet,
)


router = routers.DefaultRouter()
router.register("data-log", UserMeasurementViewSet, basename="User")
router.register("sensors", SensorViewSet, basename="Sensor")
router.register("measurements", MeasurementViewSet, basename="Measurement")
router.register("sensor-groups", SensorGroupViewSet, basename="SensorGroups")


urlpatterns = [
    path("", include(router.urls)),
]
