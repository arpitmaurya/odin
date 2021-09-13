from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        help_text='Required. Max 50 characters',
        error_messages={
            'unique': "Sorry, that username already exists. Try something else",
        },
    )
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    contact_number = models.CharField(max_length=15, unique=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.TextField(blank=True)
    dob = models.DateField()
    photo = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')
    first_name = models.CharField(max_length=50)
    is_creator = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    total_time = models.IntegerField(null=True)
    last_seen = models.DateTimeField(null=True)

    REQUIRED_FIELDS = ["email", "gender", "dob", "contact_number", "first_name"]

    def __str__(self):
        return self.username

   # def __unicode__(self):
     #   return self.email

    @property
    def get_age(self):
        today = date.today()
        age = today.year - self.dob.year
        if today.month < self.dob.month or (today.month == self.dob.month and today.day < self.dob.day):
            age -= 1
        return age

