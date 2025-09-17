from rest_framework import serializers
from .models import Device, Heartbeat
from organizations.models import Organization

class DeviceEnrollSerializer(serializers.Serializer):
    org_id = serializers.IntegerField()
    name = serializers.CharField(required=False, allow_blank=True)
    app_version = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        org = Organization.objects.get(pk=validated_data["org_id"], active=True)
        return Device.objects.create(
            org=org,
            name=validated_data.get("name",""),
            app_version=validated_data.get("app_version",""),
            status="pending",
        )

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("id","org","name","status","app_version","last_seen_at","fcm_token")

class HeartbeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heartbeat
        fields = ("battery","free_space_mb")
