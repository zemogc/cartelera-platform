from django.contrib import admin
from .models import DevicePlaylist

@admin.register(DevicePlaylist)
class DevicePlaylistAdmin(admin.ModelAdmin):
    list_display = ("id","device","playlist","assigned_at")
    list_filter = ("assigned_at",)
