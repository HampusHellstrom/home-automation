from rest_framework import serializers, status
from .models import (
    Measurement,
    Sensor,
    SensorGroup,
)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from pprint import pprint
from django.core.exceptions import PermissionDenied



class FilteredMeasurementSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        now = datetime.now()
        query_params = self.context["request"].query_params

        if "to_date" in query_params:
            to_date = datetime.fromisoformat(query_params["to_date"])
        else:
            to_date = now

        if "from_date" in query_params:
            from_date = datetime.fromisoformat(query_params["from_date"])
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

    def to_representation(self, data):
        return {
            "value": data.value,
            "timestamp": data.datetime.timestamp()*1000,
        }


class SensorMeasurementSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Sensor
        fields = (
            "name",
            "prop",
            "measurements"
        )


class SensorGroupMeasurementSerializer(serializers.ModelSerializer):
    sensors = SensorMeasurementSerializer(many=True)

    class Meta:
        model = SensorGroup
        fields = (
            "id",
            "name",
            "sensors"
        )


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = (
            "id",
            "name",
            "description",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        return Location.objects.create(user=user, **validated_data)



class SensorGroupSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True)

    class Meta:
        model = SensorGroup
        fields = (
            "id",
            "name",
            "description",
            "sensors",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        return Location.objects.create(user=user, **validated_data)



class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "id",
            "sensor",
            "value",
            "datetime",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        sensor = Sensor.objects.get(id=validated_data["sensor"].id)

        if user == sensor.user:
            return Measurement.objects.create(**validated_data)
        else:
            raise PermissionDenied("You do not have the premission to create measurements for this probe")
