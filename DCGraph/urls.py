from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('graphsocket.urls', namespace='graphsocket')),
    path('chat/', include('personalchat.urls', namespace='personalchat')),
]
