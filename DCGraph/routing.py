from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from graphsocket import routing as graphsocket_routing
from personalchat import routing as personalchat_routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            graphsocket_routing.websocket_urlpatterns +
            personalchat_routing.websocket_urlpatterns
        )
    )
})