from rest_framework import serializers
from Explore.models import TripSample


class SampleTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripSample
        exclude =['category']
        
        
