from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import (
    Measurement,
    Location,
    Device,
    Probe,
)
from .serializers import (
    LocationMeasurementSerializer,
    LocationSerializer,
    DeviceSerializer,
    ProbeSerializer,
    MeasurementSerializer,
)


# Create your views here.
class UserMeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = LocationMeasurementSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)


# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # queryset = Location.objects.all()
    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)

# Create your views here.
class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        locations = Location.objects.filter(user=self.request.user)
        return Device.objects.filter(location__in=locations)

# Create your views here.
class ProbeViewSet(viewsets.ModelViewSet):
    serializer_class = ProbeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        locations = Location.objects.filter(user=self.request.user)
        devices = Device.objects.filter(location__in=locations)
        return Probe.objects.filter(device__in=devices)


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
