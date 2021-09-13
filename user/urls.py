from .views import *
from django.urls import path


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit-profile', ProfileEditView.as_view(), name="edit-profile"),
    path('<slug:username>/', TimelineView.as_view(), name="user-timeline"),
]