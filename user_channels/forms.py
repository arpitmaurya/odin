from django import forms
from videos.models import Video
from .models import Channel

class ChannelCreateForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ["channel_name", "CHANNEL_TYPE", "channel_photo"]




class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'thumbnail', 'video_file', 'description', 'licence']

    def __init__(self, *args, **kwargs):
        super(VideoCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'item', 'placeholder': ' Video Title'})
        self.fields['thumbnail'].widget.attrs.update(
            {'class': 'drop_zone', 'placeholder': 'Thumbnail...'})
        self.fields['video_file'].widget.attrs.update(
            {'class': 'drop_zone', 'placeholder': 'Video'})
        self.fields['description'].widget.attrs.update(
            {'class': 'item', 'placeholder': 'Description'})
        self.fields['licence'].widget.attrs.update(
            {'class': 'question-answer', 'placeholder': 'Licence Policy'})

