from django.shortcuts import render
from http import cookies
import datetime
import requests
# Create your views here.



def chathome(request):
    return render(request, 'graphsocket/chathome.html')

def room(request, room_name):
    return render(request, 'graphsocket/chatroom.html', {
        'room_name': room_name
    })