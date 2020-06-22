from django.shortcuts import render
# from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from django.views.generic import ListView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.utils.datastructures import MultiValueDictKeyError
import datetime
import requests
import random
import redis
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

    def post(self, request, *args, **kwargs):
        r = redis.Redis()
        dic = {
            "Type": "Success",
            "Message": self.randomString(),
        }
        return Response(data=dic, status=status.HTTP_202_ACCEPTED)