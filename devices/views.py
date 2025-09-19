from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Device
from .serializers import DeviceEnrollSerializer, DeviceSerializer, HeartbeatSerializer
from delivery.models import DevicePlaylist
from organizations.models import Organization

# Permiso simple de admin (usaremos usuario del admin de Django por ahora)
class IsAdminUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and request.user.is_staff)

class EnrollDevice(APIView):
    permission_classes = [permissions.AllowAny]  # app puede enrolarse sin login de usuario
    def post(self, request):
        ser = DeviceEnrollSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        device = ser.save()
        return Response({"device_id": device.id, "status": device.status}, status=201)

class ApproveDevice(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, device_id: int):
        try:
            device = Device.objects.get(pk=device_id)
        except Device.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        org = device.org
        # Enforce licencia/cupo
        approved_count = Device.objects.filter(org=org, status="approved").count()
        if approved_count >= org.max_devices:
            return Response({"detail":"Cupo de dispositivos alcanzado"}, status=409)

        device.status = "approved"
        device.save(update_fields=["status"])
        return Response({"device_id": device.id, "status": device.status}, status=200)

class BlockDevice(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, device_id: int):
        try:
            device = Device.objects.get(pk=device_id)
        except Device.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        device.status = "blocked"
        device.save(update_fields=["status"])
        return Response({"device_id": device.id, "status": device.status}, status=200)

class HeartbeatView(APIView):
    permission_classes = [permissions.AllowAny]  # luego podemos exigir token de dispositivo
    def post(self, request, device_id: int):
        try:
            device = Device.objects.get(pk=device_id, status="approved")
        except Device.DoesNotExist:
            return Response({"detail": "Device not approved or not found"}, status=404)
        ser = HeartbeatSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        hb = ser.save(device=device)
        device.last_seen_at = timezone.now()
        device.save(update_fields=["last_seen_at"])
        return Response({"ok": True, "heartbeat_id": hb.id}, status=201)

class ManifestView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, device_id: int):
        try:
            device = Device.objects.get(pk=device_id, status="approved")
        except Device.DoesNotExist:
            return Response({"detail": "Device not approved or not found"}, status=404)

        # Toma la playlist asignada más reciente (si usas múltiples, aquí puedes extender)
        assignment = DevicePlaylist.objects.filter(device=device).order_by("-assigned_at").first()
        if not assignment:
            return Response({"version": timezone.now().isoformat(), "items": []})

        playlist = assignment.playlist
        items = []
        for it in playlist.items.all().order_by("order","id"):
            items.append({
                "type": it.type,
                "url": request.build_absolute_uri(it.file.url),
                "duration": it.duration if it.type == "image" else None,
                "checksum": it.checksum or "",
            })
        return Response({
            "version": timezone.now().isoformat(),
            "items": items,
        })
