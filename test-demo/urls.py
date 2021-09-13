from django.urls import path
from .views import *

urlpatterns = [
    path('bro', BroCreateView.as_view(), name="bro-create"),
    path('pop', PopCreateView.as_view(), name="pop-create"),
]
