from django.db import models
from helper.models import Creation
from Users.models import User

class Ping(Creation):
    label = models.CharField(max_length=250)
    redirect_path = models.CharField(max_length=250)
    user = models.ForeignKey(User, related_name = 'user_pings', to_field = 'email', on_delete=models.CASCADE)
    user_by = models.ForeignKey(User, to_field = 'email', on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)