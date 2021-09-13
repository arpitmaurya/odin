from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from user.models import User
from .models import FollowRequest, FollowList


def follow_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		if user_id:
			try:
				this_user = User.objects.get(pk=user_id)
				context['this_user'] = this_user
			except User.DoesNotExist:
				return HttpResponse("That user does not exist")
			try:
				follow_list = FollowList.objects.get(user=this_user)
			except FollowList.DoesNotExist:
				return HttpResponse(f"Could not find a follow list for {this_user.username}")

			# Must be our following to view list
			if user != this_user:
				if not user in follow_list.following.all() or follow_list.follower.all():
					return HttpResponse("You must be related to view their follow listings")
			followings = []  # [(following1, True), (following2, False), ...]
			followers = []
			# get the authenticated users following list
			auth_user_follow_list = FollowList.objects.get(user=user)
			for following in follow_list.following.all():
				followings.append((following, auth_user_follow_list.is_following(following)))
			for follower in follow_list.follower.all():
				followers.append((follower, auth_user_follow_list.is_follower(follower)))
			context['followings'] = followings
			context['followers'] = followers
	else:
		return HttpResponse("You must be related to view their follow listings")
	return render(request, "follow/follow_list.html", context)


def follow_requests(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		account = User.objects.get(pk=user_id)
		if account == user:
			follow_requests = FollowRequest.objects.filter(receiver=account, is_active=True)
			context['follow_requests'] = follow_requests
		else:
			return HttpResponse("You can't view another users follow requests")
	else:
		redirect("login")
	return render(request, "follow/follow_requests.html", context)


def send_follow_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = User.objects.get(pk=user_id)
			try:
				# Get any follow requests (active and not-active)
				follow_requests = FollowRequest.objects.filter(sender=user, receiver=receiver)
				# find if any of them are active (pending)
				try:
					for request in follow_requests:
						if request.is_active:
							raise Exception("You already sent them a request")
					# If none are active create a new follow request
					follow_request = FollowRequest(sender=user, receiver=receiver)
					follow_request.save()
					payload['response'] = "Request sent"
				except Exception as e:
					payload['response'] = str(e)
			except FollowRequest.DoesNotExist:
				# There are no requests so create one.
				follow_request = FollowRequest(sender=user, receiver=receiver)
				follow_request.save()
				payload['response'] = "Request sent"

			if payload['response'] == None:
				payload['response'] = "Something went wrong"
		else:
			payload['response'] = "Unable to sent a request"
	else:
		payload['response'] = "You must be authenticated to send a request"
	return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_follow_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		follow_request_id = kwargs.get("follow_request_id")
		if follow_request_id:
			follow_request = FollowRequest.objects.get(pk=follow_request_id)
			# confirm that is the correct request
			if follow_request.receiver == user:
				if follow_request:
					# found the request. Now accept it
					updated_notification = follow_request.accept()
					payload['response'] = "Request accepted"

				else:
					payload['response'] = "Something went wrong"
			else:
				payload['response'] = "That is not your request to accept"
		else:
			payload['response'] = "Unable to accept that request"
	else:
		# should never happen
		payload['response'] = "You must be authenticated to accept a request"
	return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_follower(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = User.objects.get(user=user)
				follow_list = FollowList.objects.get(pk=user_id)
				follow_list.unfollow(removee)
				payload['response'] = "Successfully removed that follower"
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove that follower"
	else:
		# should never happen
		payload['response'] = "You must be authenticated to remove a follower"
	return HttpResponse(json.dumps(payload), content_type="application/json")

def remove_following(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = User.objects.get(pk=user_id)
				follow_list = FollowList.objects.get(user=user)
				follow_list.unfollow(removee)
				payload['response'] = "Successfully removed you as follower"
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove you as follower"
	else:
		# should never happen
		payload['response'] = "You must be authenticated to remove yourself as follower"
	return HttpResponse(json.dumps(payload), content_type="application/json")



def decline_follow_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		follow_request_id = kwargs.get("follow_request_id")
		if follow_request_id:
			follow_request = FollowRequest.objects.get(pk=follow_request_id)
			# confirm that is the correct request
			if follow_request.receiver == user:
				if follow_request:
					# found the request. Now decline it
					updated_notification = follow_request.decline()
					payload['response'] = "Request declined"
				else:
					payload['response'] = "Something went wrong"
			else:
				payload['response'] = "That is not your request to decline"
		else:
			payload['response'] = "Unable to decline that request"
	else:
		# should never happen
		payload['response'] = "You must be authenticated to decline a request"
	return HttpResponse(json.dumps(payload), content_type="application/json")




def cancel_follow_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = User.objects.get(pk=user_id)
			try:
				follow_requests = FollowRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
			except FollowRequest.DoesNotExist:
				payload['response'] = "Nothing to cancel. Request does not exist"

			# There should only ever be ONE active follow request at any given time. Cancel them all just in case.
			if len(follow_requests) > 1:
				for request in follow_requests:
					request.cance()
				payload['response'] = "Request canceled"
			else:
				# found the request. Now cancel it
				follow_requests.first().cancel()
				payload['response'] = "Request canceled"
		else:
			payload['response'] = "Unable to cancel that request"
	else:
		# should never happen
		payload['response'] = "You must be authenticated to cancel a request"
	return HttpResponse(json.dumps(payload), content_type="application/json")
























