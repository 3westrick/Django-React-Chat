from rest_framework import serializers
from .models import Server, Channels


class UserInlineSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channels
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    # members = UserInlineSerializer(read_only=True, many=True)
    members = serializers.SerializerMethodField()

    # owner = UserInlineSerializer(read_only=True)
    owner = serializers.CharField(source='owner.username', read_only=True)
    channels = ChannelSerializer(source='channel_server', read_only=True, many=True)

    class Meta:
        model = Server
        fields = ['id', 'title', 'description', 'owner', 'members', 'channels']

    def get_members(self, obj):
        return obj.members.count()

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        if instance.members.count() < 1:
            data.pop('members', None)
        return data
