from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import sys
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .serializers import VideoSerializer
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.urls import reverse_lazy
from django.db.models import Q
from user_channels.models import Channel, Playlist
from .models import Video


def is_users(channel_user, logged_user):
    return channel_user == logged_user

User = get_user_model()




class VideoListView(ListView):
    model = Video
    template_name = 'videos/video.html'
    context_object_name = 'videos'
    ordering = ['-date_uploaded']

    #def videos(self, request, *args, **kwargs):
        #return self.get(self, request, *args, **kwargs)





class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['name', 'thumbnail', 'description', 'licence']
    template_name = 'videos/post_update.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)


class VideoDetailView(LoginRequiredMixin, DetailView):
    model = Video

    def get_object(self, queryset=None):
        return Video.objects.get(uuid=self.kwargs.get("uuid"))







@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
