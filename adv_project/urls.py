from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from .views import getRooms, getPlayers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    path('login/', obtain_auth_token, name="api_token_auth"),
    path('rooms/', getRooms),
    path('players/', getPlayers)
]