# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/file/(?P<file_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]