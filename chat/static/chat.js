var messageBody = document.querySelector('#messages');
messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

function scrollToBottom() {
    messageBody.scrollTop = messageBody.scrollHeight;
}