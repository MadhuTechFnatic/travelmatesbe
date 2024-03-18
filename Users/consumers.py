from helper.consumers import BaseAsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from Users.serializers import UserStatusSerializer
from Users.models import UserStatus
import rest_framework

class UserStatusConsumer(BaseAsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        if await self.user_connect():
            await self.change_user_status('add')
            await self.send_user_status()

    async def receive_json(self, content, **kwargs):
        await self.send_json(content)

    @database_sync_to_async
    def get_user_status_data(self):
        statuses = UserStatus.objects.all()
        statuses_data = UserStatusSerializer(statuses, many = True).data
        return statuses_data                
    
    async def send_user_status(self):
        data = await self.get_user_status_data()
        await self.channel_layer.group_send('main', {
            'type': 'send_user_status_data',
            'data': data,
        })
    
    @database_sync_to_async
    def change_status(self, is_online = False):
        user_status = self.user.user_status
        user_status.is_online = is_online
        user_status.save()
            
    async def add_user_to_group(self):
        await self.channel_layer.group_add('main', self.channel_name)
    
    async def remove_user_to_group(self):
        await self.channel_layer.group_discard('main', self.channel_name)
    
    async def change_user_status(self, status):
        await self.change_status(True if status == 'add' else False)
        await self.add_user_to_group() if status == 'add' else await self.remove_user_to_group()
    
    async def send_user_status_data(self, event):
        await self.send_json(content = event['data'])    

    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        await self.change_user_status('remove')
        await self.send_user_status()
        