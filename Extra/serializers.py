import humanize
from rest_framework import serializers
from Extra.models import Ping
from Users.serializers import UserFullDetailsSerializer

class PingSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Extract the context from the keyword arguments
        context = kwargs.get('context', None)
        
        # Call the super constructor
        super().__init__(*args, **kwargs)
        
        # Pass the context to the nested serializer
        if context:
            self.fields['user_by'] = UserFullDetailsSerializer(context=context)
    
    user_by = UserFullDetailsSerializer(read_only = True)
    created_at = serializers.SerializerMethodField(read_only=True)
    
    def get_created_at(self,obj):
        return humanize.naturaltime(obj.created_at)
    
    class Meta:
        model = Ping
        fields = '__all__'
        