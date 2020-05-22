from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import (
    Measurement,
    Sensor,
)
from .serializers import (
    SensorGroupMeasurementSerializer,
    SensorSerializer,
    MeasurementSerializer,
    SensorGroup,
)


# Create your views here.
class UserMeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = SensorGroupMeasurementSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SensorGroup.objects.filter(user=self.request.user)


# Create your views here.
class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # queryset = Location.objects.all()
    def get_queryset(self):
        return Sensor.objects.filter(user=self.request.user)


# Create your views here.
class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        locations = Location.objects.filter(user=self.request.user)
        devices = Device.objects.filter(location__in=locations)
        probes = Probe.objects.filter(device__in=devices)
        return Measurement.objects.filter(probe__in=probes)


class SensorGroupViewSet(viewsets.ModelViewSet):

    serializer_class = SensorGroup
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SensorGroup.objects.filter(user=self.request.user)

