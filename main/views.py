from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from posts.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
import sys
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db.models import Q
from user_channels.models import Channel, Playlist

