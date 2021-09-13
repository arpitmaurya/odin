from django.contrib import admin

from follow.models import FollowList, FollowRequest


class FollowListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FollowList


admin.site.register(FollowList, FollowListAdmin)


class FollowRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__username', 'receiver__username']
    readonly_fields = ['id']

    class Meta:
        model = FollowRequest


admin.site.register(FollowRequest, FollowRequestAdmin)












