from django.urls import path, include
from .views import *
from froala_editor import views

app_name = "blogs"

urlpatterns = [
    #user-blog-list in blog channel type view
    path('AC/<uuid:uuid>', BlogCreateView.as_view(), name="blog-create"),
    #for post type view in home thinggy regarding blogs/articles
    path('', BlogListView.as_view(), name='blogs'),
    #on a different page blog-update thinggy
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    #blog detail normal thing also including delete option
    path('<uuid:uuid>', BlogDetailView.as_view(), name='blog-detail'),
    #attachment 2 delete view
    path('<int:pk>/del/', BlogDeleteView.as_view(), name='blog-delete'),
]
