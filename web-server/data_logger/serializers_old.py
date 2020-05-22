from rest_framework import serializers, status
from .models import (
    Measurement,
    Probe,
    Device,
    Location,
)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from pprint import pprint
import dateutil
from django.core.exceptions import PermissionDenied


class FilteredMeasurementSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        now = datetime.now()
        query_params = self.context["request"].query_params

        if "to_date" in query_params:
            to_date = dateutil.parser.parse(query_params["to_date"])
        else:
            to_date = now

        if "from_date" in query_params:
            from_date = dateutil.parser.parse(query_params["from_date"])
        else:
            from_date = to_date - timedelta(days=7)

        data = data.filter(
            datetime__gte = from_date,
            datetime__lte = to_date
        )
        return super(FilteredMeasurementSerializer, self).to_representation(data)

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        list_serializer_class = FilteredMeasurementSerializer
        fields = (
            "datetime",
            "value"
        )

class ProbeMeasurementSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Probe
        fields = (
            "name",
            "unit",
            "measurements"
        )

class DeviceMeasurementSerializer(serializers.ModelSerializer):
    probes = ProbeMeasurementSerializer(many=True)

    class Meta:
        model = Device
        fields = (
            "name",
            "probes"
        )

class LocationMeasurementSerializer(serializers.ModelSerializer):
    devices = DeviceMeasurementSerializer(many=True)

    class Meta:
        model = Location
        fields = (
            "name",
            "devices"
        )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        return Location.objects.create(user=user, **validated_data)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "location",
            "name",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        location = Location.objects.get(id=validated_data["location"].id)

        if user == location.user:
            return Device.objects.create(**validated_data)
        else:
            raise PermissionDenied("You do not have the premission to create devices for this location")

class ProbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probe
        fields = (
            "id",
            "device",
            "name",
            "unit",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        device = Device.objects.get(id=validated_data["device"].id)
        location = Location.objects.get(id=device.id)

        if user == location.user:
            return Probe.objects.create(**validated_data)
        else:
            raise PermissionDenied("You do not have the premission to create probes for this device")


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "id",
            "probe",
            "value",
            "datetime",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        probe = Probe.objects.get(id=validated_data["probe"].id)
        device = Device.objects.get(id=probe.id)
        location = Location.objects.get(id=device.id)

        if user == location.user:
            return Measurement.objects.create(**validated_data)
        else:
            raise PermissionDenied("You do not have the premission to create measurements for this probe")
