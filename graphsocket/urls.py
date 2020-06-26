from django.contrib import admin
from django.urls import path
from . import views


app_name = 'graphsocket'

urlpatterns = [
    path('graph/', views.index, name='index'),
    path('chathome/', views.chathome, name='chathome'),
    path('<str:room_name>/', views.room, name='chatroom'),
]