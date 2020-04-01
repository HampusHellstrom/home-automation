from rest_framework import viewsets
from .models import Measurement
from .serializers import MeasurementSerializer, UserMeasurementsSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User

# Create your views here.
# class MeasurementViewSet(viewsets.ModelViewSet):
#     queryset = MeasurementEntry.objects.all()
#     serializer_class = MeasurementSerializer
#     authentication_classes = (TokenAuthentication,)


# Create your views here.
class UserMeasurementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserMeasurementsSerializer
    authentication_classes = (TokenAuthentication,)
