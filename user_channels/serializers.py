from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['channel_name', 'CHANNEL_TYPE', 'channel_photo', 'user']