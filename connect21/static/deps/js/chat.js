 const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + groupName + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = data.message;

        // Добавляем новое сообщение в чат
        document.querySelector('#chat-messages').innerHTML += (`
            <div class="chat-message">${message}</div>
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
        messageInputDom.value = '';  // Очищаем поле ввода
    };

    document.querySelector('#chat-message-input').onkeydown = function(e) {
        if (e.keyCode === 13) {  // Если нажата клавиша Enter
            document.querySelector('#chat-message-submit').click();  // Отправляем сообщение
        }
    };