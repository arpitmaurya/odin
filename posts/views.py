from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from .models import Post, PostFiles
import sys
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from .forms import PostCreateForm
from user_channels.models import Channel
from user_channels.forms import ChannelCreateForm
from .forms import PostCreateForm
from django.contrib import messages




def is_users(post_user, logged_user):
    return post_user == logged_user


PAGINATION_COUNT = 3
User = get_user_model()





class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'posts'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(user=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)


class PostCreateView(LoginRequiredMixin, FormView):
    form_class = PostCreateForm
    template_name = 'home.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('postfiles__files')
        content = request.POST.get('content')
        if form.is_valid():
            x = Post(user=request.user, content=content)
            x.save()
            for f in files:
                file_instance = PostFiles(post=x, files=f)
                file_instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def form_invalid(self, form):
        #If the form is invalid, render the invalid form.
        print(form.errors)
        return redirect(reverse_lazy('post-create'))

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.order_by('-date_posted')
        context['channels'] = Channel.objects.filter(user=self.request.user)
        #context['form_channel'] = ChannelCreateForm
        return context



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'posts/post_update.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)


