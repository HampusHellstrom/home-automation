from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

from django.views.generic import TemplateView

class UserView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        user = User.objects.create_user(**request.data.dict())
        Token.objects.create(user=user)
        return Response(UserSerializer(user).data)

    def delete(self, request, *args, **kwargs):
        return Response(data=UserSerializer(request.user).data)

    def update(self, request, *args, **kwargs):
        pass
