from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'graphsocket/index.html')


def chathome(request):
    return render(request, 'graphsocket/chathome.html')

def room(request, room_name):
    return render(request, 'graphsocket/chatroom.html', {
        'room_name': room_name
    })