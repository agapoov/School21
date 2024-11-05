const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + groupName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const username = data.username;

    document.querySelector('#chat-messages').innerHTML += (` 
        <div class="chat-message">
            <strong>${username}:</strong> ${message}
        </div>
    `);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};

document.querySelector('#chat-message-input').onkeydown = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};
