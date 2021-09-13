from django.urls import path

from .views import(
	send_follow_request,
	follow_requests,
	accept_follow_request,
	remove_following,
	remove_follower,
	decline_follow_request,
	cancel_follow_request,
	follow_list_view,
)

app_name = 'follow'

urlpatterns = [
	path('list/<user_id>', follow_list_view, name='list'),
	path('follower_remove/', remove_follower, name='remove-follower'),
	path('following_remove/', remove_following, name='remove-following'),
    path('follow_request/', send_follow_request, name='follow-request'),
    path('follow_request_cancel/', cancel_follow_request, name='follow-request-cancel'),
    path('follow_requests/<user_id>/', follow_requests, name='follow-requests'),
    path('follow_request_accept/<follow_request_id>/', accept_follow_request, name='follow-request-accept'),
    path('follow_request_decline/<follow_request_id>/', decline_follow_request, name='follow-request-decline'),
]