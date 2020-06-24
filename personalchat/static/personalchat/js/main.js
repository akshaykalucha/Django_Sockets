console.log("js loaded for user")

const ID = JSON.parse(document.getElementById('id').textContent);


const chatsocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/user/'
    + ID
    + '/'
)


chatsocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data, "received from admin")
    try{
        if(data.myMsg.data){
            document.querySelector('#chat-log').value += (data.myMsg.data + '\n');
            if(data.myMsg.imp){
                console.log(data.myMsg.imp)
            }
        }
    }catch{
        console.log("")
    }
    try{
        if(data.message.adminMessage){
            Cookies.set('foo', data.message.from)
            document.querySelector('#chat-log').value += (data.message.adminMessage + '\n');
        }
    }catch{
        console.log("")
    }
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

var sent = 0

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
    if(sent===0){
        axios.post(`/chat/admin/${makeid(233)}/${ID}/`, {
            firstName: 'Fred',
            lastName: 'Flintstone'
        })
            .then((response) => {
            console.log(response);
        }, (error) => {
            console.log(error);
        });
    }
    sent += 1
    console.log(sent)
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    var encmsg = stringToBinary(message)
    var channelName = ID
    // channelName = stringToBinary(channelName)
    channelName = string2Bin(channelName)
    channelName = btoa(channelName)
    console.log(channelName)
    var binarybyte = string2Bin(encmsg)
    if(Cookies.get('foo')){
        channelVal = Cookies.get('foo')
    }
    else{
        channelVal = null
    }
    chatsocket.send(JSON.stringify({
        'message': message,
        'type': 'byUser',
        'sendToAdmin': channelVal
    }));
    messageInputDom.value = '';
};