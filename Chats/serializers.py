import humanize
from rest_framework import serializers
from Chats.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField(read_only=True)
    
    def get_time(self, obj):
        return humanize.naturaltime(obj.created_at)
    
    class Meta:
        model = Chat
        exclude = ['id']
        

class MessageSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField(read_only=True)
    
    def get_time(self, obj):
        return humanize.naturaltime(obj.created_at)

    class Meta:
        model = Chat
        exclude = ['id']
        