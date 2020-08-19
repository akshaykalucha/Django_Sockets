from django.shortcuts import render
from http import cookies
import datetime
import requests
# Create your views here.

def index(request):
    session = request.COOKIES['servercookie']
    print(session, "A cookie got by server")
    response = render(request, "graphsocket/index.html")
    response.set_cookie('servercookie', "this is from server", samesite="Strict", domain='127.0.0.1', path="/graph/")
    response.set_cookie("serverGlobal", "this is for the website but available to all paths")
    return response

