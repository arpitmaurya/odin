from django.contrib import admin
from .models import Post, PostFiles


class PostFilesAdmin(admin.StackedInline):
    model = PostFiles

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostFilesAdmin]

    class Meta:
        model = Post

@admin.register(PostFiles)
class PostImageAdmin(admin.ModelAdmin):
    pass