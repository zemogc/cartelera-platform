from django.db import models
from playlists.models import Playlist

class MediaItem(models.Model):
    TYPE = [("image","Image"),("video","Video")]
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="items")
    type = models.CharField(max_length=10, choices=TYPE)
    file = models.FileField(upload_to="uploads/")  # o "content/", o deja "" para raíz de media
    
    duration = models.PositiveIntegerField(default=8)  # segundos (u opcional en videos)
    order = models.PositiveIntegerField(default=0)
    checksum = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ("order","id")

    def __str__(self):
        return f"{self.playlist} | {self.type} | {self.file.name}"
