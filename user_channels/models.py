from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from user.models import User
import uuid

class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="channels")
    channel_name = models.CharField(max_length=50, null=False, blank=False)
    CHANNEL_TYPE_CHOICES = (
        ('A', 'Article'),
        ('S', 'Audio'),
        ('V', 'Video'),
    )
    channel_photo = models.ImageField(upload_to="channel_photo")
    channel_cover_photo = models.ImageField(upload_to="channel_cover_photo", null=False, blank=False, default=None)
    CHANNEL_TYPE = models.CharField(max_length=1, choices=CHANNEL_TYPE_CHOICES)
    subscribers = models.BigIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.channel_name

    #def get_absolute_url(self):
        #return reverse('video-channel', kwargs={'url': self.url})




class Playlist(models.Model):
    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True, related_name="playlists")
    playlist_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.playlist_name
