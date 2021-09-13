from django.contrib import admin

from .models import Video
from user_channels.models import Playlist

admin.site.register(Playlist)
admin.site.register(Video)
