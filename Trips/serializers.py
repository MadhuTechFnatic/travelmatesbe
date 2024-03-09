from rest_framework import serializers
from Trips.models import Trip
from django.contrib.humanize.templatetags.humanize import naturaltime
import datetime

class TripSerializer(serializers.ModelSerializer):
    human_readable_time = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.CharField(required=False)
    comments = serializers.IntegerField(required=False)
    likes = serializers.IntegerField(required=False)
    requests = serializers.IntegerField(required=False)
    connected_users = serializers.IntegerField(required=False)
    time = serializers.TimeField(format = '%I:%M %p')

    def get_human_readable_time(self, obj):
        # Convert date to datetime object
        datetime_obj = datetime.datetime.combine(obj.date, obj.time)
        return naturaltime(datetime_obj)
        
    
    class Meta:
        fields = '__all__'
        model = Trip