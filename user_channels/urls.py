from django.urls import path
from .views import *

app_name = "user_channels"

urlpatterns = [
    path('VC/<uuid:uuid>', VideoChannelView.as_view(), name='video-channel'),
    path('VC-dashboard/<uuid:uuid>', Dashboard.as_view(), name='dashboard'),
    path('VC-edit/<uuid:uuid>', UpdateChannel.as_view(), name='edit'),
    path('VC-delete/<uuid:uuid>', DeleteChannel.as_view(), name='delete'),
    path('create-channel', CreateChannel.as_view(), name="home"),
]