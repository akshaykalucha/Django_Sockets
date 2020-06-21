from django.contrib import admin
from django.urls import path
from . import views


app_name = 'personalchat'

urlpatterns = [
    path('me/<int:id>/', views.index, name='index'),
]