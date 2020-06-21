console.log("js loaded")

const ID = JSON.parse(document.getElementById('id').textContent);

console.log(ID, "this is id of room")


const chatsocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/me/'
    + ID
    + '/'
)

console.log(chatsocket)


chatsocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.message + '\n');
};

chatsocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatsocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};