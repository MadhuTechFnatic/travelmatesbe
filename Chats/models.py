from django.db import models
from helper.models import Creation, UIID
from Users.models import User


class Chat(Creation, UIID):
    from_user = models.ForeignKey(User, related_name= 'user_chats_from', to_field='email', on_delete= models.CASCADE) 
    to_user = models.ForeignKey(User, related_name= 'user_chats_to', to_field='email', on_delete= models.CASCADE)
    
    
class Message(Creation, UIID):
    chat = models.ForeignKey(Chat, to_field='uiid', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= 'travel_mate_messages', to_field='travel_mate_id', on_delete= models.CASCADE) 
    user_name = models.CharField(max_length=50)
    message = models.TextField()
    status = models.BooleanField(default='', blank = True)

    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = self.user.user_details.nick_name
        return super().save(*args, **kwargs)
    
