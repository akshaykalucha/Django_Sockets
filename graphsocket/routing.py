from django.conf.urls import url
from django.urls import path
from . import consumer
from django.urls import re_path

websocket_urlpatterns = [
    path('ws/polData/', consumer.DataConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatConsumer), 
]