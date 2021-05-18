"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from chat import consumers
from django.urls import path


from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

ws_pattern= [
    path('ws/room/<room_code>/' , consumers.ChatConsumer.as_asgi())
]

application= ProtocolTypeRouter(
    {
        'websocket':(URLRouter(ws_pattern))
    }
)

