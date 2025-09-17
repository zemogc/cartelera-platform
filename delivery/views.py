# delivery/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser  # builtin DRF

from devices.models import Device
from playlists.models import Playlist
from .serializers import AssignPlaylistSerializer
from .models import DevicePlaylist

class AssignPlaylistView(APIView):
    permission_classes = [IsAdminUser]  # requiere usuario staff con JWT

    def post(self, request, device_id: int):
        # validar request
        ser = AssignPlaylistSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        playlist_id = ser.validated_data["playlist_id"]

        # buscar device y playlist
        try:
            device = Device.objects.get(pk=device_id, status="approved")
        except Device.DoesNotExist:
            return Response({"detail": "Device no existe o no está aprobado"}, status=404)

        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist no encontrada"}, status=404)

        # validar misma organización
        if playlist.org_id != device.org_id:
            return Response({"detail": "Playlist y device no pertenecen a la misma organización"}, status=400)

        # crear asignación
        DevicePlaylist.objects.create(device=device, playlist=playlist)
        return Response({"ok": True, "device_id": device.id, "playlist_id": playlist.id}, status=201)
