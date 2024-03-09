from django.db import models # Import JSONField
from helper.models import Creation, UIID
from helper.choices import TRIP_CATEGORIES
from helper.validations import validate_trip_image_size
from helper.functions import get_user_name
from Users.models import User

class Trip(Creation, UIID):
    title = models.CharField(max_length=100)
    
    address_from = models.CharField(max_length=100)
    address_to = models.CharField(max_length=100)
    
    trip_cover_img = models.ImageField(upload_to='trip_cover_images', null=True, blank=True, validators=[validate_trip_image_size])
    category = models.CharField(max_length=30, choices=TRIP_CATEGORIES)
    date = models.DateField()
    time = models.TimeField()
    group_size = models.SmallIntegerField(default=2)
    distance = models.IntegerField(null=True)
    
    # Optional fields
    description = models.TextField(blank=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)
    
    # Readonly fields
    connected_users = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field = 'email', related_name='user_trips')
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title    
    
    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = get_user_name(self.user)
        return super().save(*args, **kwargs)


