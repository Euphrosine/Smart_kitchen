# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .consumers import FanStatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/fan_status/$', FanStatusConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
