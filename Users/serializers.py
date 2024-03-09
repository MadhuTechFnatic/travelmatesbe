from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserDetail, User
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
        user_detail = user.user_details.first()
        # Generate or retrieve token
        tokens_data = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        user_detail_data = UserDetailSerializer(user_detail).data
        user_data.update(user_detail_data)
        return {
            'token_data': tokens_data,
            'user_data': user_data,
        }

class UserDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)
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