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
from .models import *
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
import urllib.request,json
# from .models import Article, Category, Source , Headlines
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


class testPostgres(APIView):

    def post(self, request):
        name = request.data.get("name")

        nameObjs = TestingUser.objects.get(name=name)
        print(nameObjs.name)

        dic = {
            "Type": "Sucecss",
            "data": nameObjs.name
        }
        return Response(data=dic, status=status.HTTP_200_OK)

class testRedis(APIView):
    r = redis.Redis()

    def post(self, request):

        name = request.data.get("name")
        nameObjs = self.r.hget("TestingUser", "name")
        dic = {
            "Type": "Sucecss",
            "data": nameObjs
        }
        return Response(data=dic, status=status.HTTP_200_OK)


api_key = None

source_url= None

cat_url= None

def configure_request(app):
    global api_key, source_url, cat_url
    api_key = app.config['NEWS_API_KEY']
    source_url= app.config['NEWS_API_SOURCE_URL']
    cat_url=app.config['CAT_API_URL']


def get_source():
    get_source_url= source_url.format(api_key)
    # print(get_source_url)
    with urllib.request.urlopen(get_source_url) as url:
        get_sources_data = url.read()
        get_sources_response = json.loads(get_sources_data)

        source_results = None

        if get_sources_response['sources']:
            source_results_list = get_sources_response['sources']
            source_results = process_results(source_results_list)

    return source_results

def process_results(source_list):
    source_results = []
    for source_item in source_list:
        id = source_item.get('id')
        name = source_item.get('name')
        description = source_item.get('description')
        url = source_item.get('url')
        if id:
            source_object = Source(id,name,description,url)
            source_results.append(source_object)

    return source_results

def article_source(id):
    article_source_url = 'https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(id,api_key)
    print(article_source_url)
    with urllib.request.urlopen(article_source_url) as url:
        article_source_data = url.read()
        article_source_response = json.loads(article_source_data)

        article_source_results = None

        if article_source_response['articles']:
            article_source_list = article_source_response['articles']
            article_source_results = process_articles_results(article_source_list)


    return article_source_results

def process_articles_results(news):
    article_source_results = []
    for article in news:
        author = article.get('author')
        description = article.get('description')
        time = article.get('publishedAt')
        url = article.get('urlToImage')
        image = article.get('url')
        title = article.get ('title')

        if url:
            article_objects = Article(author,description,time,image,url,title)
            article_source_results.append(article_objects)

    return article_source_results

def get_category(cat_name):
    get_category_url = cat_url.format(cat_name,api_key)
    print(get_category_url)
    with urllib.request.urlopen(get_category_url) as url:
        get_category_data = url.read()
        get_cartegory_response = json.loads(get_category_data)

        get_cartegory_results = None

        if get_cartegory_response['articles']:
            get_cartegory_list = get_cartegory_response['articles']
            get_cartegory_results = process_articles_results(get_cartegory_list)

    return get_cartegory_results
def get_headlines():
    get_headlines_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey={}'.format(api_key)
    print(get_headlines_url)
    with urllib.request.urlopen(get_headlines_url) as url:
        get_headlines_data = url.read()
        get_headlines_response = json.loads(get_headlines_data)

        get_headlines_results = None

        if get_headlines_response['articles']:
            get_headlines_list = get_headlines_response['articles']
            get_headlines_results = process_articles_results(get_headlines_list)

    return get_headlines_results