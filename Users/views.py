import requests
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Users.models import User, Follow
from Trips.serializers import TripSerializer
from .serializers import (FollowUnFollowSerializer, UserDetailSerializer, UserLoginSerializer,
    UserRegisterSerializer)

class LoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    authentication_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        return Response(user_data, status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = []
    
    
class UserDetailAddView(CreateAPIView):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    
    
class FollowUnFollowView(UpdateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowUnFollowSerializer
    
    def update(self, request, email):
        user = User.objects.get(email=email)
        follower = request.user
        try: 
            Follow.objects.get().delete()
        except Follow.DoesNotExist:
            Follow.objects.create(user=user, follower=follower)
        
        return Response(None, 202)
    
    
class UserStatsCountView(APIView):
    
    def get_is_following_by_current_user(self, request, user):
        current_user = request.user
        return user.user_followers.filter(follower = current_user).exists()
        
    def get_is_follower_to_current_user(self, request, user):
        current_user = request.user
        return current_user.user_followers.filter(follower = user).exists()
    
    def get(self, request, email):
        if email is None or email == '':
            user = request.user
        user = User.objects.get(email=email)
        followers = user.user_followers.count()
        followings = user.user_followings.count()
        trips = user.user_trips.count()
        data = {
            'followers': followers,
            'followings': followings,
            'trips' : trips,
            'is_following_by_current_user' : self.get_is_following_by_current_user(request, user),
            'is_follower_to_current_user' : self.get_is_follower_to_current_user(request, user)
        }
        return Response(data, 200)
    
    
class UserFollowersView(APIView):
    
    def get(self, request, email):
        if email is None:
            user = request.user
        user = User.objects.get(email=email)
        followers = user.user_followers.all()
        data = FollowUnFollowSerializer(followers, many = True).data,
        return Response(data, 200)
    
    
class UserFollowingsView(APIView):
    
    def get(self, request, email):
        if email is None:
            user = request.user
        user = User.objects.get(email=email)
        followings = user.user_followings.all()
        data = FollowUnFollowSerializer(followings, many = True).data,
        return Response(data, 200)