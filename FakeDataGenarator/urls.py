from django.urls import path
from .views import *

urlpatterns = [
     path('explore_sample_trip_data', ExploreTripSampleData.as_view()),
     path('fake_trips', TripsFakeData.as_view())
]