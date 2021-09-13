from django import forms
from .models import Post
from django.forms import ClearableFileInput

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            'files': ClearableFileInput(attrs={'multiple': True}),
        }

