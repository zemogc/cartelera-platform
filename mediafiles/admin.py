from django.contrib import admin
from .models import MediaItem

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("id","playlist","type","file","duration","order")
    list_filter = ("type","playlist")
    search_fields = ("file",)
