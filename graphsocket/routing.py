from django.conf.urls import url
from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/polData/', consumer.DataConsumer)   
]