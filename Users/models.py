from django.db import models
from helper.models import Creation, UIID
from helper.validations import validate_image_dimensions, validate_image_size
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    groups = None
    user_permissions = None
    first_name = None
    last_name = None
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserDetail(Creation):
    user = models.OneToOneField(User, related_name = 'user_details', to_field = 'email', on_delete = models.CASCADE)
    nick_name = models.CharField(max_length=50, null=True, blank=True)
    phone_no = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField()
    gender = models.CharField(default = 'male' ,max_length=20)
    profile_pic = models.ImageField(upload_to='profiles', null=True, blank=True, validators=[validate_image_dimensions, validate_image_size])
    
    followers = models.PositiveIntegerField(default=0, null=True, blank=True)
    following = models.PositiveIntegerField(default=0, null=True, blank=True)
    trips = models.PositiveIntegerField(default=0, null=True, blank = True)
    
    def __str__(self):
        return self.nickName
    
    
class Follow(Creation, UIID):
    user = models.ForeignKey(User, related_name = 'user_followers', to_field = 'email', on_delete = models.CASCADE)
    follower = models.ForeignKey(User, related_name = 'user_followings', to_field = 'email', on_delete = models.CASCADE)

