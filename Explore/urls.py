from django.urls import path
from .views import *

urlpatterns = [
    path('sample_trips/<str:category>',TripSampleDataView.as_view()),
    path('categories',TripSampleCategoryView.as_view())
]