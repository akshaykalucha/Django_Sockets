from django.shortcuts import render
# from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from django.views.generic import ListView
from .models import *
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from http import cookies
import requests
import random
from django.conf import settings
import redis
import jwt
import string
import random
import http
from django.db.models.functions import Lower
from django.core.exceptions import \
    (ObjectDoesNotExist, MultipleObjectsReturned)
from datetime import timedelta
import pandas as pd
from pyfcm import FCMNotification
# from DCGraph.settings import JWT_SECRET_KEY
# Create your views here.



def index(request, id):
    # session = request.COOKIES['serverGlobal']
    # print(session, "A cookie got by server")
    return render(request, 'personalchat/index.html', {
        'id': id
    })

def admin(request, id):
    return render(request, 'personalchat/myindex.html', {
        'id': id
    })



class sendSocketRes(APIView):

    def randomString(self):
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(random.randint(10,20)))

    # def test_cookie_parameters(self):
    #         key = 'some_cookie'
    #         value = 'some_value'
    #         secure = True
    #         domain = 'test.com'
    #         rest = {'HttpOnly': True}

    #         jar = requests.cookies.RequestsCookieJar()
    #         jar.set(key, value, secure=secure, domain=domain, rest=rest)

    #         assert len(jar) == 1
    #         assert 'some_cookie' in jar

    #         cookie = list(jar)[0]
    #         assert cookie.secure == secure
    #         assert cookie.domain == domain
    #         assert cookie._rest['HttpOnly'] == rest['HttpOnly']

    def post(self, request, *args, **kwargs):
        r = redis.Redis()
        dic = {
            "Type": "Success",
            "Message": self.randomString(),
        }
        response = Response(data=dic, status=status.HTTP_202_ACCEPTED)
        response.set_cookie('last_connection', datetime.datetime.now(), httponly=True, samesite='Lax')
        return response




class pendingMessages(APIView):

    def randomString(self):
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(random.randint(10,20)))

    def post(self, request, *args, **kwargs):
        r = redis.Redis()
        dic = {
            "Type": "Success",
            "Message": self.randomString(),
        }
        response = Response(data=dic, status=status.HTTP_202_ACCEPTED)
        #response.set_cookie('last_connection', datetime.datetime.now(), httponly=True, samesite='Lax')
        return response