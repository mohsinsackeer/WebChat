var main = function(){

    var socket = io();
    var msg_btn = document.getElementById('message-btn');
    var messages = $('#messages');

    // Sending the message
    msg_btn.addEventListener("click", function(event){
        event.preventDefault();

        text_msg = $("#input").val();
        console.log(text_msg);
        socket.emit('send message', {message : text_msg});
        $("#input").val("");
    });

    // socket custom events
    socket.on('connect', function(){
        socket.emit('my event', {data: 'I am connected!'});
    });

    socket.on('server broadcast', function(msg){
        var item = $('<li>');
        item.text(msg);
        messages.append(item);
        $("html, body").animate({ scrollTop: $(document).height() }, 1000);
    });
    
};

$(document).ready(main);