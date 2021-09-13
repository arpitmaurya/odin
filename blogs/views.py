from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import sys
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from user_channels.models import Channel, Playlist
from .models import Blog
from .forms import BlogCreateForm


def is_users(channel_user, logged_user):
    return channel_user == logged_user

User = get_user_model()



class BlogCreateView(LoginRequiredMixin, FormView):
    model = Blog
    form_class = BlogCreateForm
    template_name = 'blogs/channel.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        content = request.POST.get('content')
        thumbnail = request.FILES.get('thumbnail')
        name = request.POST.get('name')
        licence = request.POST.get('licence')
        playlist = request.POST.get('playlist')
        if playlist is "":
            playlist = None
        if form.is_valid():
            Blog(channel=self.channel(), content=content, thumbnail=thumbnail, name=name, licence=licence, playlist=playlist).save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def channel(self):
        return get_object_or_404(Channel, uuid=self.kwargs.get("uuid"))

    def channel_blogs(self):
        return Blog.objects.filter(channel=self.channel())

    def get_context_data(self, **kwargs):
        kwargs['channel'] = self.channel()
        kwargs['blogs'] = self.channel_blogs()
        return super(BlogCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(BlogCreateView, self).form_valid(form)



class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blog.html'
    context_object_name = 'videos'
    ordering = ['-date_uploaded']



class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['name', 'thumbnail', 'description', 'licence']
    template_name = 'blogs/blog_update.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)



class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'

    def get_object(self, queryset=None):
        return Blog.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        kwargs['blog'] = self.get_object()
        return super(BlogDetailView, self).get_context_data(**kwargs)



class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.playlist.channel.user:
            return True
        return False




