(() => {
    const MAX_CHARACTERS = 1000; // Максимальное количество символов
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + groupUuid + '/' // Используем groupSlug
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        const username = data.username;
        const isUserMessage = data.is_user_message;
        const timestamp = data.timestamp;
        const messageClass = isUserMessage ? 'user-message' : 'other-message';

        // Добавляем сообщение в контейнер
        const chatMessages = document.querySelector('#chat-messages');
        const messageHTML = `
            <div class="chat-message ${messageClass}">
                <div class="message-header">
                    <strong class="username">${username}</strong>
                </div>
                <div class="message-content">
                    ${message}
                </div>
                <span class="timestamp">${timestamp}</span>
            </div>`;
        chatMessages.insertAdjacentHTML('beforeend', messageHTML);

        // Прокрутка вниз
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    document.querySelector('#chat-message-submit').onclick = function () {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;

        if (message.trim() === '') return;

        chatSocket.send(
            JSON.stringify({
                message: message
            })
        );

        messageInputDom.value = '';
        messageInputDom.style.height = 'auto'; // Сбрасываем высоту поля
    };

    document.querySelector('#chat-message-input').onkeydown = function (e) {
        if (e.keyCode === 13 && !e.shiftKey) {
            e.preventDefault();
            document.querySelector('#chat-message-submit').click();
        }
    };

    // Ограничение на количество символов и автоматическая подстройка размера поля ввода
    const textarea = document.querySelector('#chat-message-input');
    textarea.addEventListener('input', function () {
        // Обрезаем текст, если он превышает лимит
        if (this.value.length > MAX_CHARACTERS) {
            this.value = this.value.slice(0, MAX_CHARACTERS);
        }

        this.style.height = 'auto'; // Сбрасываем высоту
        this.style.height = `${this.scrollHeight}px`; // Устанавливаем высоту по содержимому
    });

    // Прокрутка вниз при загрузке страницы
    window.onload = function () {
        const chatMessages = document.querySelector('#chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };
})();