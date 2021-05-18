from django.contrib import admin

# Register your models here.
from .models import Room , Chats

admin.site.register(Room)
admin.site.register(Chats)
