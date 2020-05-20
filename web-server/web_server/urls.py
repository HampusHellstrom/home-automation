from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('data-logger/', include("data_logger.urls")),
    path('login/', obtain_auth_token),
    path('users/', UserView.as_view()),
]
