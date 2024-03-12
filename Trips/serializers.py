from rest_framework import serializers
from Trips.models import *
from django.contrib.humanize.templatetags.humanize import naturaltime
import datetime
from Users.serializers import UserFullDetailsSerializer
import humanize

class TripSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        # Extract the context from the keyword arguments
        context = kwargs.get('context', None)
        
        # Call the super constructor
        super().__init__(*args, **kwargs)
        
        # Pass the context to the nested serializer
        if context:
            self.fields['trip_user'] = UserFullDetailsSerializer(read_only = True, context=context)
    
    trip_user = UserFullDetailsSerializer(read_only = True)
    human_readable_time = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.CharField(required=False)
    comments = serializers.IntegerField(required=False)
    likes = serializers.IntegerField(required=False)
    requests = serializers.IntegerField(required=False)
    connected_users = serializers.SerializerMethodField(read_only=True)
    connected_users_count = serializers.SerializerMethodField(read_only=True)
    time = serializers.TimeField(format = '%I:%M %p')
    like_status = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    dislikes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    requests_count = serializers.SerializerMethodField(read_only=True)

    def get_human_readable_time(self, obj):
        # Convert date to datetime object
        datetime_obj = datetime.datetime.combine(obj.date, obj.time)
        return naturaltime(datetime_obj)
    
    def get_like_status(self, obj):
        user = self.context['request'].user
        try :        
            like = TripLike.objects.get(user=user, trip=obj)      
            return like.status
        except:
            return None
        
    def get_likes_count(self, obj):
        return obj.trip_likes.filter(status = 'like').count()

    def get_dislikes_count(self, obj):
        return obj.trip_likes.filter(status = 'dislike').count()
    
    def get_comments_count(self, obj):
        return obj.trip_comments.count()
    
    def get_requests_count(self, obj):
        return obj.trip_requests.count()
    
    def get_connected_users(self, obj):
        return UserFullDetailsSerializer(obj.connected_users, many = True, context = self.context).data
    
    def get_connected_users_count(self, obj):
        return obj.connected_users.count()
    
    class Meta:
        fields = '__all__'
        model = Trip
        
class TripLikeSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        # Extract the context from the keyword arguments
        context = kwargs.get('context', None)
        
        # Call the super constructor
        super().__init__(*args, **kwargs)
        
        # Pass the context to the nested serializer
        if context:
            self.fields['user'] = UserFullDetailsSerializer(context=context)
    
    user = UserFullDetailsSerializer(read_only = True)
    
    class Meta:
        fields = '__all__'
        model = TripLike
        
class TripCommentSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        # Extract the context from the keyword arguments
        context = kwargs.get('context', None)
        
        # Call the super constructor
        super().__init__(*args, **kwargs)
        
        # Pass the context to the nested serializer
        if context:
            self.fields['user'] = UserFullDetailsSerializer(context=context)
    
    
    replies = serializers.SerializerMethodField(read_only = True)
    user = UserFullDetailsSerializer(read_only = True)
    time = serializers.SerializerMethodField(read_only = True)
    
    def get_time(self, obj):
        return humanize.naturaltime(obj.created_at)
    
    def get_replies(self, obj):
        replies = obj.trip_comments_replies.all()
        if replies.count() == 0:
            return []
        return TripCommentSerializer(replies).data

    class Meta:
        fields = '__all__'
        model = TripComment
        
class TripRequestSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        # Extract the context from the keyword arguments
        context = kwargs.get('context', None)
        
        # Call the super constructor
        super().__init__(*args, **kwargs)
        
        # Pass the context to the nested serializer
        if context:
            self.fields['user'] = UserFullDetailsSerializer(context=context)
    
    user = UserFullDetailsSerializer(read_only = True)
    
    class Meta:
        fields = '__all__'
        model = TripRequest
        