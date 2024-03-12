from django.db import models # Import JSONField
from helper.models import Creation, UIID
from helper.choices import LIKE_CHOICES, TRIP_CATEGORIES
from helper.validations import validate_trip_image_size
from helper.functions import get_user_name
from Users.models import User

class Trip(Creation, UIID):
    title = models.CharField(max_length=100)
    
    address_from = models.CharField(max_length=100)
    address_to = models.CharField(max_length=100)
    
    trip_cover_img = models.ImageField(upload_to='trip_cover_images', null=True, blank=True, validators=[validate_trip_image_size])
    category = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    group_size = models.SmallIntegerField(default=2)
    distance = models.IntegerField(null=True)
    
    # Optional fields
    description = models.TextField(blank=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)

    # Readonly fields
    is_published = models.BooleanField(default=False)
    connected_users = models.ManyToManyField(User, related_name='user_connected_trips')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field = 'email', related_name='user_trips')
    comments = models.PositiveIntegerField(default=0)
    requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title    
    
    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = get_user_name(self.user)
        return super().save(*args, **kwargs)


class TripLike(Creation, UIID):
    trip = models.ForeignKey(Trip, related_name = 'trip_likes', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = 'liked_trips', to_field = 'email', on_delete = models.CASCADE)
    status = models.CharField(max_length = 10, choices = LIKE_CHOICES, default = 'like')

class TripComment(Creation, UIID):
    trip = models.ForeignKey(Trip, related_name = 'trip_comments', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = 'commented_trips', to_field = 'email', on_delete = models.CASCADE)
    comment = models.TextField()


class TripReplyComment(Creation, UIID):
    comment = models.ForeignKey(TripComment, related_name = 'trip_comments_replies', on_delete = models.CASCADE)
    reply_comment = models.ForeignKey(TripComment, related_name = 'replied_comments', on_delete = models.CASCADE)


class TripRequest(Creation, UIID):
    trip = models.ForeignKey(Trip, related_name = 'trip_requests', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = 'requested_trips', to_field = 'email', on_delete = models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    