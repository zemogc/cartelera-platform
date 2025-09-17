from django.db import models
from organizations.models import Organization

class Device(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("blocked", "Blocked"),
    ]
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    fcm_token = models.TextField(blank=True, default="")
    last_seen_at = models.DateTimeField(null=True, blank=True)
    app_version = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"{self.org.name} | {self.name or self.pk} | {self.status}"

class Heartbeat(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="heartbeats")
    battery = models.PositiveSmallIntegerField(null=True, blank=True)
    free_space_mb = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
