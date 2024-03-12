from django.db.models.signals import post_save
from django.dispatch import receiver
from Trips.models import TripComment, TripLike, TripRequest
from Extra.models import Ping

@receiver(post_save, sender=TripLike)
def create_like_ping(instance, **kwargs):
    trip = instance.trip
    status = instance.status
    Ping.objects.create(
        user = trip.user,
        user_by = instance.user,
        redirect_path = 'p',
        label = f"{instance.user.user_details.nick_name} {'Liked' if status == 'like' else 'Disliked'} your '{trip.title}' trip"
    )

@receiver(post_save, sender=TripComment)
def create_comment_ping(instance, **kwargs):
    trip = instance.trip
    Ping.objects.create(
        user = trip.user,
        user_by = instance.user,
        redirect_path = 'p',
        label = f"{instance.user.user_details.nick_name} Commented on your '{trip.title}' trip"
    )

@receiver(post_save, sender=TripRequest)
def create_comment_ping(instance, **kwargs):
    trip = instance.trip
    Ping.objects.create(
        user = trip.user,
        user_by = instance.user,
        redirect_path = 'p',
        label = f"{instance.user.user_details.nick_name} Requested to join your '{trip.title}' trip"
    )