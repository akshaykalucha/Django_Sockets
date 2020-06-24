from django.contrib import admin
from django.urls import path
from . import views
from .views import *


app_name = 'personalchat'

urlpatterns = [
    path('me/<int:id>/', views.index, name='index'),
    path('admin/chat/user/<int:id>', views.admin, name='admin'),
    path(r'admin/<slug:slug>/<int:id>/', sendSocketRes.as_view(), name="chat-admin"),
    path(r'admin/<slug:slug>/get-pending-messages/', pendingMessages.as_view(), name="pendingMessages")
]