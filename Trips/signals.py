from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from Trips.models import *
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
def create_comment_ping(instance, created, **kwargs):
    if created:
        trip = instance.trip
        Ping.objects.create(
            user = trip.user,
            user_by = instance.user,
            redirect_path = 'p',
            label = f"{instance.user.user_details.nick_name} Requested to join your '{trip.title}' trip"
        )    

@receiver(post_save, sender=TripRequest)
def create_comment_ping(instance, created, **kwargs):
    if not created:
        trip = instance.trip
        requested_user = instance.user
        Ping.objects.create(
            user = requested_user,
            user_by = trip.user,
            redirect_path = 'p',
            label = f"{trip.user.user_details.nick_name}, has accepted your request to join '{trip.title}' trip."
        )
    
@receiver(pre_delete, sender=TripRequest)
def informing_trip_cancel_to_connected_users(instance, **kwargs):
    trip = instance.trip
    Ping.objects.create(
        user = instance.user,
        user_by = trip.user,
        redirect_path = '/',
        label = f"{trip.user.user_details.nick_name}, was rejected your '{trip.title}' trip request. We apologize for any inconvenience caused."
    )
    
@receiver(pre_delete, sender=Trip)
def informing_trip_cancel_to_connected_users(instance, **kwargs):
    for connected_user in instance.connected_users:
        Ping.objects.create(
            user = connected_user,
            user_by = instance.user,
            redirect_path = '/',
            label = f"Hi {connected_user.user.user_details.nick_name}, our '{instance.trip.title}' trip has been cancelled due to some reasons. We apologize for any inconvenience caused."
        )
    
