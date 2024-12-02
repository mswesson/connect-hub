from rest_framework import serializers

from .models import Client, ClientConnections


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "user_id",
            "phone",
            "invitation_code",
        ]
        read_only_fields = ["invitation_code", "user_id", "id"]


class ClientProfileSerializer(serializers.ModelSerializer):
    connections_invited_clients = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            "id",
            "phone",
            "invitation_code",
            "someone_invitation_code",
            "connections_invited_clients",
        ]

    def get_connections_invited_clients(self, obj):
        connections = ClientConnections.objects.filter(inviter_client=obj)
        return [connection.invited_client.phone for connection in connections]


class ClientLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "phone",
        ]
