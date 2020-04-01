from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import UserMeasurementViewSet


router = routers.DefaultRouter()
router.register("", UserMeasurementViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
