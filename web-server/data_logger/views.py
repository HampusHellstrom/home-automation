from django.contrib.auth.models import User
from django.core import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Measurement,
    Sensor,
    SensorGroup,
)
from .serializers import (
    SensorGroupMeasurementSerializer,
    SensorSerializer,
    MeasurementSerializer,
    SensorGroupSerializer,
)


def response(status=200, msg="OK"):
    message = {
        "status": status,
        "message": msg,
    }
    return Response(status=status, data=message)


def required_fields(headers=[], params=[], data=[]):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            for header in headers:
                if header not in request.headers:
                    return Response(status=400, data={"message":f"Missing header {header}, required headers: {headers}"})

            for param in params:
                if param not in request.params:
                    return Response(status=400, data={"message":f"Missing param {param}, required params: {params}"})

            for data_key in data:
                if isinstance(request.data, list):
                    for element in request.data:
                        if data_key not in element:
                            return Response(status=400, data={"message":f"Missing data key {data_key}, required keys: {data}"})
                elif isinstance(request.data, dict):
                    if data_key not in request.data:
                        return Response(status=400, data={"message":f"Missing data key {data_key}, required keys: {data}"})
            func(self, request, *args, **kwargs)
            return None
        return wrapper
    return decorator


class SensorView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = Sensor.objects.filter(user=self.request.user)
        return Response(data=SensorSerializer(queryset, many=True).data)

    @required_fields(data=["description", "name", "prop"])
    def post(self, request, *args, **kwargs):
        sensor = Sensor.objects.create(user=request.user, **request.data)
        return Response(data=SensorSerializer(sensor).data)


class UserMeasurementView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    required_fields(params=["sensor_groups"])
    def get(self, request, *args, **kwargs):
        queryset = SensorGroup.objects.filter(
            user=request.user,
            id__in=request.query_params["sensor_groups"],
        )
        return Response(
            data=SensorGroupMeasurementSerializer(
                queryset,
                many=True,
                context={"request": self.request}
            ).data
        )


class SensorGroupView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = SensorGroup.objects.filter(user=self.request.user)
        return Response(data=SensorGroupSerializer(queryset, many=True).data)

    @required_fields(data=["name", "sensors"])
    def post(self, request, *args, **kwargs):
        data = request.data
        sensors = data.pop("sensors")

        # Verify all sensors belong to user
        for sensor in sensors:
            sensor = Sensor.objects.get(id=sensor)
            if sensor.user != request.user:
                return response(status=401, msg=f"Unauthorized to add sensor {sensor.id} to sensor group")
        sensor_group = SensorGroup.objects.create(user=request.user, **data)
        sensor_group.sensors.add(*sensors)
        return Response(data=SensorGroupSerializer(sensor_group).data)

    def delete(self, request, *args, **kwargs):
        sensor_group = SensorGroup.objects.get(id=request.data["id"])
        if sensor_group.user != request.user:
            return response(status=401, msg=f"Unauthorized to delete sensor group {sensor_group.id}")
        out_data = SensorGroupSerializer(sensor_group).data
        sensor_group.delete()
        return Response(status=200, data=out_data)

    def put(self, request, *args, **kwargs):
        data = request.data

        # Verify all sensors belong to user
        for sensor in data.get("sensors", []):
            sensor = Sensor.objects.get(id=sensor)
            if sensor.user != request.user:
                return response(status=401, msg=f"Unauthorized to add sensor {sensor.id} to sensor group")
        sensor_group = SensorGroup.objects.get(id=data["id"])
        if "name" in data:
            sensor_group.name = data["name"]
        if "description" in data:
            sensor_group.description = data["description"]
        if "sensors" in data:
            print("Got here, trying to delete sensors")
            sensor_group.sensors.clear()
            sensor_group.sensors.add(*data["sensors"])
        sensor_group.save()
        return Response(data=SensorGroupSerializer(sensor_group).data)



class MeasurementView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return response(status=415, msg="Endpoint only accepts json")

        if isinstance(request.data, dict):
            measurements = [request.data]
        elif isinstance(request.data, (list, tuple)):
            measurements = request.data
        else:
            return response(status=415, msg="Endpoint only accepts json")

        created_measurements = []
        for measurement in measurements:
            if "sensor" not in measurement or "value" not in measurement:
                return response(status=400, msg="Measurement needs to contain both the keys 'sensor' and 'value'")
            try:
                sensor = Sensor.objects.get(id=measurement["sensor"])
            except Exception as e:
                return response(status=400, msg=f"Cannot find sensor {measurement['sensor']}")
            if sensor.user != request.user:
                return response(status=401, msg=f"Unauthorized to add measurements for sensor {sensor.id}")

            measurement["sensor"] = sensor

        for measurement in measurements:
            created_measurements.append(Measurement.objects.create(**measurement))


        return Response(data=MeasurementSerializer(created_measurements, many=True).data)


    def delete(self, request, *args, **kwargs):
        measurement = Measurement.objects.get(id=request.data["id"])
        if measurement.sensor.user != request.user:
            return response(status=401, msg=f"Unauthorized to delete sensor group {measurement.id}")
        out_data = SensorGroupSerializer(measurement).data
        measurement.delete()
        return Response(status=200, data=out_data)

