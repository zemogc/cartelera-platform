from django.db import models
from devices.models import Device
from playlists.models import Playlist

class DevicePlaylist(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="assignments")
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("device","playlist")

    def __str__(self):
        return f"{self.device} -> {self.playlist}"
