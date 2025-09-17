from django.contrib import admin
from .models import Playlist

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id","org","name","is_active")
    list_filter = ("org","is_active")
    search_fields = ("name",)
