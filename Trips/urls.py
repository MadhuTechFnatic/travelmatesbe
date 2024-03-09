from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripCategoriesView, TripViewSet

router = DefaultRouter()
router.register('trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('trips/meta/categories', TripCategoriesView.as_view()),
]
