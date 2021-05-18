from django.db import models
from base_rest.models import BaseModel
from django.contrib.auth.models import User





class Room(BaseModel):
    room_code = models.CharField(max_length=100)
    current_online = models.ManyToManyField(User)


class Chats(BaseModel):
    room = models.ForeignKey(Room , on_delete=models.CASCADE , related_name ="room")
    text_message = models.TextField(blank=True , null=True)
    sender = models.ForeignKey( User,null=True, blank=True  ,on_delete=models.CASCADE , related_name="user")
    
    
    