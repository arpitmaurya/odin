from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import Notification


class FollowList(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="following")
	follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="follower")

	# set up the reverse relation to GenericForeignKey
	notifications = GenericRelation(Notification)

	def __str__(self):
		return self.user.username

	def add_follower(self, account):
		"""
		Add a new follower
		"""
		if not account in self.follower.all():
			self.follower.add(account)
			self.save()

			content_type = ContentType.objects.get_for_model(self)

			self.notifications.create(
				target=self.user,
				from_user=account,
				redirect_url=f"{settings.BASE_URL}/account/{account.pk}/",
				verb=f"{account.username} is now following you",
				content_type=content_type,
			)
			self.save()

			# Create a private chat (or activate an old one)
			#chat = find_or_create_private_chat(self.user, account)
			#if not chat.is_active:
			#	chat.is_active = True
			#	chat.save()

	def remove_follower(self, account):
		"""
		Remove a follower
		"""
		if account in self.follower.all():
			self.follower.remove(account)

			# Deactivate the private chat between these two users
			#chat = find_or_create_private_chat(self.user, account)
			#if chat.is_active:
			#	chat.is_active = False
			#	chat.save()

	def add_following(self, account):
		"""
		Add a new following user
		"""
		if not account in self.following.all():
			self.following.add(account)
			self.save()

			content_type = ContentType.objects.get_for_model(self)

			self.notifications.create(
				target=self.user,
				from_user=account,
				redirect_url=f"{settings.BASE_URL}/account/{account.pk}/",
				verb=f"You are now following {account.username}",
				content_type=content_type,
			)
			self.save()

			# Create a private chat (or activate an old one)
			#chat = find_or_create_private_chat(self.user, account)
			#if not chat.is_active:
			#	chat.is_active = True
			#	chat.save()

	def remove_following(self, account):
		"""
		Remove a following user
		"""
		if account in self.following.all():
			self.following.remove(account)

			# Deactivate the private chat between these two users
			#chat = find_or_create_private_chat(self.user, account)
			#if chat.is_active:
			#	chat.is_active = False
			#	chat.save()

	def unfollow(self, removee):
		"""
		Initiate the action of unfollowing someone
		"""
		# Remove user from following list
		self.remove_following(removee)

		# Remove yourself from follower list
		follower_list = FollowList.objects.get(user=removee)
		follower_list.remove_follower(self.user)

		content_type = ContentType.objects.get_for_model(self)

		# Create notification for removee
		follower_list.notifications.create(
			target=removee,
			from_user=self.user,
			redirect_url=f"{settings.BASE_URL}/account/{self.user.pk}/",
			verb=f"{self.user.username} no longer follows you",
			content_type=content_type,
		)

		# Create notification for remover
		self.notifications.create(
			target=self.user,
			from_user=removee,
			redirect_url=f"{settings.BASE_URL}/account/{removee.pk}/",
			verb=f"You no longer follow {removee.username}.",
			content_type=content_type,
		)

	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FollowList"

	def is_follower(self, follower):
		"""
		Is this a follower?
		"""
		if follower in self.follower.all():
			return True
		return False

	def is_following(self, following):
		"""
		Am I a follower?
		"""
		if following in self.following.all():
			return True
		return False



class FollowRequest(models.Model):
	"""
	A follow request consists of two main parts:
		1. SENDER
			- Person sending/initiating the request
		2. RECIVER
			- Person receiving the request
	"""

	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

	is_active = models.BooleanField(blank=False, null=False, default=True)

	timestamp = models.DateTimeField(auto_now_add=True)

	notifications = GenericRelation(Notification)

	def __str__(self):
		return self.sender.username

	def accept(self):
		"""
		Accept a request.
		Update both SENDER and RECEIVER follow lists.
		"""
		receiver_follower_list = FollowList.objects.get(user=self.receiver)
		if receiver_follower_list:
			content_type = ContentType.objects.get_for_model(self)

			# Update notification for RECEIVER
			receiver_notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
			receiver_notification.is_active = False
			receiver_notification.redirect_url = f"{settings.BASE_URL}/account/{self.sender.pk}/"
			receiver_notification.verb = f"You accepted {self.sender.username}'s follow request"
			receiver_notification.timestamp = timezone.now()
			receiver_notification.save()

			receiver_follower_list.add_follower(self.sender)

			sender_following_list = FollowList.objects.get(user=self.sender)
			if sender_following_list:

				# Create notification for SENDER
				self.notifications.create(
					target=self.sender,
					from_user=self.receiver,
					redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
					verb=f"{self.receiver.username} accepted your follow request",
					content_type=content_type,
				)

				sender_following_list.add_following(self.receiver)
				# sender_following_list.save()
				self.is_active = False
				self.save()
			return receiver_notification # we will need this later to update the realtime notifications


	def decline(self):
		"""
		Decline a follow request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.is_active = False
		self.save()

		content_type = ContentType.objects.get_for_model(self)

		# Update notification for RECEIVER
		notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
		notification.is_active = False
		notification.redirect_url = f"{settings.BASE_URL}/account/{self.sender.pk}/"
		notification.verb = f"You declined {self.sender}'s follow request"
		notification.from_user = self.sender
		notification.timestamp = timezone.now()
		notification.save()

		# Create notification for SENDER
		self.notifications.create(
			target=self.sender,
			verb=f"{self.receiver.username} declined your follow request",
			from_user=self.receiver,
			redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
			content_type=content_type,
		)

		return notification


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()

		content_type = ContentType.objects.get_for_model(self)

		# Create notification for SENDER
		self.notifications.create(
			target=self.sender,
			verb=f"You cancelled the follow request to {self.receiver.username}.",
			from_user=self.receiver,
			redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
			content_type=content_type,
		)

		notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
		notification.verb = f"{self.sender.username} cancelled the follow request sent to you"
		#notification.timestamp = timezone.now()
		notification.read = False
		notification.save()

	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FollowRequest"


@receiver(post_save, sender=FollowRequest)
def create_notification(sender, instance, created, **kwargs):
	if created:
		instance.notifications.create(
			target=instance.receiver,
			from_user=instance.sender,
			redirect_url=f"{settings.BASE_URL}/account/{instance.sender.pk}/",
			verb=f"{instance.sender.username} sent you a follow request",
			content_type=instance,
		)














