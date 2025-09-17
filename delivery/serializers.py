from rest_framework import serializers

class AssignPlaylistSerializer(serializers.Serializer):
    playlist_id = serializers.IntegerField()
