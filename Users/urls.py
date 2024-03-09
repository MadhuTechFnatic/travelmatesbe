from django.urls import path
from .views import RegisterView, LoginView, UserDetailAddView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('user_details', UserDetailAddView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', TokenBlacklistView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]