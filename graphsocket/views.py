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

def oauth_session(request, state=None, token=None):
    if settings.DISCORD_REDIRECT_URI is not None:
        redirect_uri = settings.DISCORD_REDIRECT_URI
    else:
        redirect_uri = request.build_absolute_uri(
            reverse('discord_bind_callback'))
    scope = (['email', 'guilds.join'] if settings.DISCORD_EMAIL_SCOPE
             else ['identity', 'guilds.join'])
    return OAuth2Session(settings.DISCORD_CLIENT_ID,
                         redirect_uri=redirect_uri,
                         scope=scope,
                         token=token,
                         state=state)

@login_required
def index(request):
    # Record the final redirect alternatives
    if 'invite_uri' in request.GET:
        request.session['discord_bind_invite_uri'] = request.GET['invite_uri']
    else:
        request.session['discord_bind_invite_uri'] = (
                settings.DISCORD_INVITE_URI)

    if 'return_uri' in request.GET:
        request.session['discord_bind_return_uri'] = request.GET['return_uri']
    else:
        request.session['discord_bind_return_uri'] = (
                settings.DISCORD_RETURN_URI)

    # Compute the authorization URI
    oauth = oauth_session(request)
    url, state = oauth.authorization_url(settings.DISCORD_BASE_URI +
                                         settings.DISCORD_AUTHZ_PATH)
    request.session['discord_bind_oauth_state'] = state
    return HttpResponseRedirect(url)

@login_required
def callback(request):
    def decompose_data(user, token):
        data = {
            'uid': user['id'],
            'username': user['username'],
            'discriminator': user['discriminator'],
            'email': user.get('email', ''),
            'avatar': user.get('avatar', ''),
            'access_token': token['access_token'],
            'refresh_token': token.get('refresh_token', ''),
            'scope': ' '.join(token.get('scope', '')),
        }
        for k in data:
            if data[k] is None:
                data[k] = ''
        try:
            expiry = datetime.utcfromtimestamp(float(token['expires_at']))
            if settings.USE_TZ:
                expiry = make_aware(expiry)
            data['expiry'] = expiry
        except KeyError:
            pass
        return data
    def bind_user(request, data):
        uid = data.pop('uid')
        count = DiscordUser.objects.filter(uid=uid).update(user=request.user,
                                                           **data)
        if count == 0:
            DiscordUser.objects.create(uid=uid,
                                       user=request.user,
                                       **data)

    response = request.build_absolute_uri()
    state = request.session['discord_bind_oauth_state']
    if 'state' not in request.GET or request.GET['state'] != state:
        return HttpResponseForbidden()
    oauth = oauth_session(request, state=state)
    token = oauth.fetch_token(settings.DISCORD_BASE_URI +
                              settings.DISCORD_TOKEN_PATH,
                              client_secret=settings.DISCORD_CLIENT_SECRET,
                              authorization_response=response)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

bot.run(TOKEN)



@run_async
def connection_chat(bot: Bot, update: Update):

    chat = update.effective_chat
    user = update.effective_user

    spam = spamfilters(update.effective_message.text, update.effective_message.from_user.id, update.effective_chat.id)
    if spam == True:
        return
    conn = connected(bot, update, chat, user.id, need_admin=True)

    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type != "private":
            return
        chat = update.effective_chat
        chat_name = update.effective_message.chat.title

    if conn:
        message = "You are currently connected with {}.\n".format(chat_name)
    else:
        message = "You are currently not connected in any group.\n"
    send_message(update.effective_message, message, parse_mode="markdown")


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


@run_async
@dev_plus
@gloggable
def addsupport(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""
    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "Demoting status of this SUDO to SUPPORT"
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        message.reply_text("This user is already a SUDO.")
        return ""

    if user_id in WHITELIST_USERS:
        rt += "Promoting Disaster level from WHITELIST USER to SUPPORT USER"
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)
    data['supports'].append(user_id)
    SUPPORT_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(rt + f"\n{user_member.first_name} was added as a Support User!")

    log_message = (f"#SUPPORT\n"
                   f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                   f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = "<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message

def addsudo(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        message.reply_text("This member is already my SUDO.")
        return ""

    if user_id in SUPPORT_USERS:
        rt += "This user is already a SUPPORT USER."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

@run_async
@dev_plus
@gloggable
def addwhitelist(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

@run_async
@dev_plus
@gloggable
def removewhitelist(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WHITELIST_USERS:
        message.reply_text("Demoting to normal user")
        WHITELIST_USERS.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (f"#UNWHITELIST\n"
                       f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                       f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a whitelist!")
        return ""
