from .models import FollowRequest

def get_follow_request_or_false(sender, receiver):
	try:
		return FollowRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
	except FollowRequest.DoesNotExist:
		return False