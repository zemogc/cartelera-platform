from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "max_devices", "license_exp_at", "active")
    search_fields = ("name",)
