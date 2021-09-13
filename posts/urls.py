from django.urls import path
from .views import *
from django.urls import include





urlpatterns = [
    #path('post/', PostListView.as_view(), name='posts'),
    path('', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/del/', PostDeleteView.as_view(), name='post-delete'),
]
