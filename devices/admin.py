from django.contrib import admin
from .models import Device, Heartbeat

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id","org","name","status","last_seen_at","app_version")
    list_filter = ("org","status")
    search_fields = ("name",)

@admin.register(Heartbeat)
class HeartbeatAdmin(admin.ModelAdmin):
    list_display = ("id","device","battery","free_space_mb","created_at")
    list_filter = ("created_at",)
