from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('trips/likes/<pk>', TripLikeView.as_view()),
    path('trips/comments/<pk>', TripCommentView.as_view()),
    path('trips/requests/<pk>', TripRequestView.as_view()),
    path('trips/requests/accept-reject/<request_pk>', TripRequestAcceptRejectView.as_view()),
    path('trips/meta/categories', TripCategoriesView.as_view()),
]
