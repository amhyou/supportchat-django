from django.urls import re_path,path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/server/<str:stream>',ChatConsumer.as_asgi())
]