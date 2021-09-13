from django import forms
from user_channels.models import Channel

class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['channel_name', 'CHANNEL_TYPE']
