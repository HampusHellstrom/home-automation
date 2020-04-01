from rest_framework import serializers, status
from .models import Measurement, Probe, Device, Location
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = (
            "datetime",
            "value"
        )
#     def create(self, validated_data):
#         user = self.context['request'].user
#         return Measurement.objects.create(user= user, **validated_data)


class ProbeSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Probe
        fields = (
            "name",
            "measurements"
        )

class DeviceSerializer(serializers.ModelSerializer):
    probes = ProbeSerializer(many=True)

    class Meta:
        model = Device
        fields = (
            "name",
            "probes"
        )

class LocationSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True)

    class Meta:
        model = Location
        fields = (
            "name",
            "devices"
        )

class UserMeasurementsSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "username",
            "locations"
        )
