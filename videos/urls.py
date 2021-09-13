from django.urls import path
from .views import *

app_name = "videos"

urlpatterns = [
    path('videoq', VideoListView.as_view(), name='videos'),
    #path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('video/<uuid:url>', VideoDetailView.as_view(), name='video-detail'),
    #path('post/<int:pk>/del/', PostDeleteView.as_view(), name='post-delete'),

]