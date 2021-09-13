from django.db import models
from user_channels.models import Playlist, Channel
from django.shortcuts import reverse
import uuid
from froala_editor.fields import FroalaField

class Blog(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_DEFAULT, null=True, blank=True, default=None, related_name="blogs")
    channel = models.ForeignKey(Channel, on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    name = models.CharField(max_length=150, null=False, blank=False)
    thumbnail = models.ImageField(upload_to='blog_thumbnails/')
    content = FroalaField()
    LICENCE_CHOICES = (
        ('U', 'Universal'),
        ('S', 'Universal/Adult'),
        ('A', 'Adult'),
        ('X', 'XXX-Content'),
    )
    licence = models.CharField(max_length=1, choices=LICENCE_CHOICES, null=False)
    date_uploaded = models.DateField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    good = models.PositiveBigIntegerField(default=0)
    bad = models.PositiveBigIntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return "blog/" + str(self.uuid)


