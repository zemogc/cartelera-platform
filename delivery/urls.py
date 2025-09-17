# delivery/urls.py
from django.urls import path
from .views import AssignPlaylistView

urlpatterns = [
    path("devices/<int:device_id>/assign-playlist/", AssignPlaylistView.as_view(), name="assign-playlist"),
]
