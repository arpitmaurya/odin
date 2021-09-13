from django.db import models

from user.models import User
from django.utils.timezone import now
from django.conf import settings

class Bro(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bros")
    body = models.TextField()
    created_at = models.DateTimeField(default=now)

class Pop(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pops")
    body = models.TextField()
    created_at = models.DateTimeField(default=now)