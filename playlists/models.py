from django.db import models
from organizations.models import Organization

class Playlist(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="playlists")
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.org.name}:{self.name}"
