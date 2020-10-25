from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import (
    MeasurementView,
    SensorGroupView,
    # SensorGroupViewSet,
    SensorView,
    UserMeasurementView,
)


# router = routers.DefaultRouter()
# router.register("sensor-groups2", SensorGroupViewSet, basename="SensorGroups")


urlpatterns = [
    # path("", include(router.urls)),
    path("data-log/", UserMeasurementView.as_view()),
    path("measurements/", MeasurementView.as_view()),
    path("sensor-groups/", SensorGroupView.as_view()),
    path("sensors/", SensorView.as_view()),
]
