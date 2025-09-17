from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=120)
    max_devices = models.PositiveIntegerField(default=20)
    license_exp_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name