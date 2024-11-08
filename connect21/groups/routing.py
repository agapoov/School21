from django.urls import path, re_path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<group_name>\w+)/$', ChatConsumer.as_asgi()),
]
