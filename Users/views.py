from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from Users.models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserDetailSerializer

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