from django.conf.urls import url
from django.urls import path
from . import consumer
from django.urls import re_path

websocket_urlpatterns = [
    path('ws/chat/user/<int:personId>/', consumer.ChatConsumer)
]