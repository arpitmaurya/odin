from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Blog

class BlogCreateForm(forms.ModelForm):
  content = forms.CharField(widget=FroalaEditor)
  class Meta:
    model = Blog
    fields = ['name', 'thumbnail', 'content', 'licence', 'playlist']