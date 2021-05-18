  
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from .models import Chats, Room

# @database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user_id = (self.scope["query_string"].decode("utf-8")).split('=')[1]
        self.user = get_user(user_id)
    
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.group_name= 'room_%s' % self.room_name
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        
        data = {'type' : 'connected' }
        
        async_to_sync(self.channel_layer.group_send)(
                'room_%s' % self.room_name,{
                    'type':'send_online_status',
                    'value': json.dumps(data),
            }
        )
        
        self.send(text_data=json.dumps({
            'payload': 'connected',
        }))
        
    def disconnect(self,close_code):
        room_obj = Room.objects.filter(room_code = self.room_name).first()
        room_obj.current_online.remove(self.user)
        room_obj.save()
        print('dis')
        print(room_obj.current_online.all())
        print('dis')
        
        data = {'type' : 'connected' }
        
        async_to_sync(self.channel_layer.group_send)(
                'room_%s' % self.room_name,{
                    'type':'send_online_status',
                    'value': json.dumps(data),
                    
            }
        )
        
        
        
    
    def receive(self,text_data):
        data = json.loads(text_data)
        
        room_obj = Room.objects.filter(room_code = self.room_name).first()
        Chats.objects.create(room = room_obj,
            text_message = data.get('text_message'),
            sender = self.user)
        
    
        data['sender'] = self.user.username
        data['type'] = 'message'
        
        async_to_sync(self.channel_layer.group_send)(
                'room_%s' % self.room_name,{
                    'type':'send_message',
                    'value': json.dumps(data),
            }
        )
        
    def send_message(self , text_data):
        data = json.loads(text_data['value']) 
        self.send(text_data = json.dumps({
            'payload': data
        }))
        
        
    def send_online_status(self , text_data):
        data = json.loads(text_data['value']) 
        
        room_obj = Room.objects.filter(room_code = self.room_name).first()
        room_obj.current_online.add(self.user)
        room_obj.save()
        online_users = []
        
        print( room_obj.current_online.all())
        
        for online_user in room_obj.current_online.all():
            online_users.append({
                'user' : online_user.username,
                'user_id' : online_user.id 
            })
            
        data['online_users'] = online_users
        
        
        self.send(text_data = json.dumps({
            'payload': data
        }))
  