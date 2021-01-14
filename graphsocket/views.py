from django.shortcuts import render
from http import cookies
import datetime
import requests
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from django.db.models import Q
from django.contrib import messages

import requests
from requests_oauthlib import OAuth2Session

from discord_bind.models import DiscordUser, DiscordInvite
from discord_bind.conf import settings
import logging
logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    session = request.COOKIES['servercookie']
    print(session, "A cookie got by server")
    response = render(request, "graphsocket/index.html")
    response.set_cookie('servercookie', "this is from server", samesite="Strict", domain='127.0.0.1', path="/graph/")
    response.set_cookie("serverGlobal", "this is for the website but available to all paths")
    return response

def chathome(request):
    return render(request, 'graphsocket/chathome.html')

def room(request, room_name):
    return render(request, 'graphsocket/chatroom.html', {
        'room_name': room_name
    })


desired = [s for s in servers if country.lower() in s[i].lower()]
found = len(desired)
print("Found " + str(found) + " servers for country " + country)
if found == 0:
    exit(1)

supported = [s for s in desired if len(s[-1]) > 0]
print(str(len(supported)) + " of these servers support OpenVPN")
# We pick the best servers by score
winner = sorted(supported, key=lambda s: float(s[2].replace(",", ".")), reverse=True)[0]

print("\n== Best server ==")
pairs = list(zip(labels, winner))[:-1]
for (l, d) in pairs[:4]:
    print(l + ": " + d)

print(pairs[4][0] + ": " + str(float(pairs[4][1]) / 10 ** 6) + " MBps")
print("Country: " + pairs[5][1])

print("\nLaunching VPN...")
_, path = tempfile.mkstemp()

f = open(path, "w")
f.write(base64.b64decode(winner[-1]).decode())
f.write(
    "\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf"
)
f.close()

x = subprocess.Popen(["sudo", "openvpn", "--config", path])

try:
    while True:
        time.sleep(600)
# termination with Ctrl+C
except BaseException:
    try:
        x.kill()
    except BaseException:
        pass
    while x.poll() != 0:
        time.sleep(1)
    print("\nVPN terminated")