from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from Extra.models import Ping
from Users.models import Follow

@receiver(post_save, sender=Follow)
def create_like_ping(instance, **kwargs):
    Ping.objects.create(
        user = instance.user,
        user_by = instance.follower,
        redirect_path = 'p',
        label = f"{instance.follower.user_details.nick_name} Started following you"
    )
    
@receiver(pre_delete, sender=Follow)
def create_like_ping(instance, **kwargs):
    Ping.objects.create(
        user = instance.user,
        user_by = instance.follower,
        redirect_path = 'p',
        label = f"{instance.follower.user_details.nick_name} Unfollowed you"
    )
