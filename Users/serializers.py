from django.contrib.auth import authenticate
import django.contrib.humanize.templatetags.humanize
import django.db
import humanize
from rest_framework import serializers
from .models import Follow, User, UserDetail
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        # Authenticate the user
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid email or password.')
        user_detail = user.user_details
        # Generate or retrieve token
        tokens_data = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        context = self.context
        context['request'].user = user
        user_detail_data = UserDetailSerializer(user_detail, context = context).data
        user_data.update(user_detail_data)
        return {
            'token_data': tokens_data,
            'user_data': user_data,
        }

class UserDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%B %Y', read_only=True)
    is_follower_to_current_user = serializers.SerializerMethodField(read_only=True)
    is_following_by_current_user = serializers.SerializerMethodField(read_only=True)
    
    
    def get_is_following_by_current_user(self, obj):
        current_user = self.context['request'].user
        user = obj.user
        return user.user_followers.filter(follower = current_user).exists()
        
    def get_is_follower_to_current_user(self, obj):
        current_user = self.context['request'].user
        user = obj.user
        return current_user.user_followers.filter(follower = user).exists()
    
    class Meta:
        model = UserDetail
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'nick_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserFullDetailsSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(read_only = True)
    
    def get_user_details(self, obj):
        user_details = obj.user_details
        return UserDetailSerializer(user_details, context = self.context).data         
    
    class Meta :
        model = User
        fields = ['email', 'user_details', ]
        
        
class FollowUnFollowSerializer(serializers.ModelSerializer):
    user = UserFullDetailsSerializer()
    follower = UserFullDetailsSerializer()
    
    class Meta :
        model = Follow
        fields = '__all__'