var socket = io();
var input = document.getElementById("message_input");

chatHistory = [
  {"role": "system", "content": "You are a helpful assistant. You can call functions to help your answer. Only use the functions you have been provided with. Don't use markdown to format your answer. Always use HTML tags. Be a friend and always respond in the same tone as the user. You can search the web to answer the user when necessary."},
]

socket.on('message', function(data) {
    console.log('Received message:', data);
    var messages = document.getElementById('messages')
    var message = document.createElement('div')
    message.innerHTML = data.content.replace(/\n/g, "<br />");
    message.className = 'system-message';
    chatHistory.push(data);
    messages.appendChild(message)
    message.scrollIntoView();
});

function sendMessage() {
    var input = document.getElementById("message_input");
    var messages = document.getElementById('messages');
    var message = document.createElement('div');
    message.innerHTML = input.value.replace(/\n/g, "<br />");
    message.className = 'user-message';  // Add the user-message class to user messages
    chatHistory.push({"role": "user", "content": input.value});
    messages.appendChild(message);
    message.scrollIntoView();
    socket.emit('message', chatHistory);
    input.value = ''
}

input.addEventListener("keydown", function(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault(); 
    sendMessage();
  }
  return false;
});