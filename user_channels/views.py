from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, FormView
from videos.models import Video
from .models import Channel, Playlist
from .forms import ChannelCreateForm, VideoCreateForm
from django.contrib.auth import get_user_model


def is_users(channel_user, logged_user):
    return channel_user == logged_user

User = get_user_model()

class CreateChannel(LoginRequiredMixin, CreateView):
    model = Channel
    form_class = ChannelCreateForm
    template_name = 'channel/form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreateChannel, self).get_context_data(**kwargs)
        context['channels'] = Channel.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(CreateChannel, self).form_valid(form)



class VideoChannelView(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoCreateForm
    template_name = 'videos/channel.html'
    #success_url = '/'

    #def get_object(self, queryset=None):
        #return Channel.objects.get(uuid=self.kwargs.get("uuid"))

    #def get_queryset(self):
        #return Channel.objects.filter(uuid=self.kwargs['uuid'])

    def channel(self):
        return get_object_or_404(Channel, uuid=self.kwargs.get("uuid"))
    def channel_videos(self):
        #return get_object_or_404(Video, playlist__channel=self.channel())
        return Video.objects.filter(playlist__channel=self.channel())

    def get_context_data(self, **kwargs):
        logged_user = self.request.user
        visible_channel = self.channel()
        #Only show user_profile if privacy is not anonymous and user still exists or is alive. Adjust in privacy feature. To be built
        #kwargs['user_profile'] = visible_user
        #Post this in the user detail view or some shiz
        kwargs['channel'] = self.channel()
        kwargs['videos'] = self.channel_videos()
        return super(VideoChannelView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class Dashboard(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'channel/dashboard.html'
    context_object_name = 'videos'
    ordering = ['-date_uploaded']


class UpdateChannel(LoginRequiredMixin, UpdateView):
    model = Channel
    template_name = 'channel/edit.html'
    fields = ['channel_name', ]

    def channel(self):
        return get_object_or_404(Channel, uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        playlists = Playlist.objects.filter(channel=self.channel())
        kwargs['playlists'] = playlists
        return super(UpdateChannel, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteChannel(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Channel
    success_url = '/'
    template_name = 'channel/delete.html'

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)

    def get_object(self, queryset=None):
        return get_object_or_404(Channel, uuid=self.kwargs.get("uuid"))










