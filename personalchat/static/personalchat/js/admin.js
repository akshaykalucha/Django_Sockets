console.log("js loaded")

const ID = JSON.parse(document.getElementById('id').textContent);


const chatsocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/user/'
    + Math.floor(Math.random() * 564738) + 546876
    + '/'
)



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



function stringToBinary(str, spaceSeparatedOctets) {
    function zeroPad(num) {
        return "00000000".slice(String(num).length) + num;
    }
    str = toString(str)
    return str.replace(/[\s\S]/g, function(str) {
        str = zeroPad(str.charCodeAt().toString(2));
        return !1 == spaceSeparatedOctets ? str : str + " "
    });
};

function string2Bin(str) {
    str = toString(str)
    var result = [];
    for (var i = 0; i < str.length; i++) {
      result.push(str.charCodeAt(i));
    }
    return result;
  }
  
function bin2String(array) {
return String.fromCharCode.apply(String, array);
}

function returnarrayobjs(arr){
    return arr.join('')
}

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
 }
 

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    var encmsg = stringToBinary(message)
    var channelName = ID
    // channelName = stringToBinary(channelName)
    channelName = string2Bin(channelName)
    channelName = btoa(channelName)
    console.log(channelName)
    var binarybyte = string2Bin(encmsg)
    chatsocket.send(JSON.stringify({
        'type': 'byAdmin',
        'message': message,
        'channelId': ID
    }));
    messageInputDom.value = '';
};