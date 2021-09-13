from django.db import models
from user_channels.models import Playlist
from autoslug import AutoSlugField
from django.shortcuts import reverse
import uuid

class Video(models.Model):
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    playlist = models.ForeignKey(Playlist, on_delete=models.SET_DEFAULT, null=True, blank=True, default="playlists", related_name="videos")
    name = models.CharField(max_length=150, null=False, blank=False)
    video_file = models.FileField(null=False, blank=False)
    thumbnail = models.ImageField(null=False, blank=False)
    description = models.TextField()
    LICENCE_CHOICES = (
        ('U', 'Universal'),
        ('S', 'Universal/Adult'),
        ('A', 'Adult'),
        ('X', 'XXX-Content'),
    )
    licence = models.CharField(max_length=1, choices=LICENCE_CHOICES, null=False)
    date_uploaded = models.DateField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    good = models.BigIntegerField(default=0)
    bad = models.BigIntegerField(default=0)
    views = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('video-detail', kwargs={'url': self.url})


