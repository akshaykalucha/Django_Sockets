from django.shortcuts import render

# Create your views here.

def index(request, id):
    return render(request, 'personalchat/index.html', {
        'id': id
    })