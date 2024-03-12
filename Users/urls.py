from django.urls import path
from .views import *
from Trips.views import UserTripsView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('user_details', UserDetailAddView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', TokenBlacklistView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    
    ## follows and stats paths
    path('follow-unfollow/<email>',FollowUnFollowView.as_view()),
    path('user-stats-count/<email>', UserStatsCountView.as_view()),
    path('user-followers/<email>', UserFollowersView.as_view()),
    path('user-followings/<email>', UserFollowingsView.as_view()),    
    path('user-trips/<email>', UserTripsView.as_view()),
]