const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + groupName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const username = data.username;
    const timestamp = data.timestamp;  // Получаем timestamp

    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');

    messageElement.innerHTML = `
        <strong>${username}:</strong> ${message}
        <span class="timestamp">${timestamp}</span>
    `;

    document.querySelector('#chat-messages').appendChild(messageElement);
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
