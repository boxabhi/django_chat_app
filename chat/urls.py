
from django.urls import path
from .views import *

urlpatterns = [
    path('' , home , name="home"),
    path('chat/<room_code>/' , chat , name="chat")
]
