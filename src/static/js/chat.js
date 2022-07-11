var main = function(){
    console.log('chat.js is active!');

    var socket = io();
    var receiver;
    var sender;


    var names= ["Adwaith", "Mohsin","DK"];
    var list = $('#chat-list');
    var str = "https://png.pngitem.com/pimgs/s/150-1503945_transparent-user-png-default-user-image-png-png.png"
    names.forEach((i)=>{
        var li = $('<li>');
        var div = $('<div>');
        div.addClass("check_class");
        div.prepend('<img src = "'+str+'"  alt="contact_image">');
        div.append('<span >'+i+'</span>');
        li.append(div);
        list.append(li);
    });

    var send_btn = document.getElementById('send_bt');
    var msg_text =$('#msg_input');
    //var msgArray =[];
    var messages = $('#messages');

    socket.on("set-username", function(data){
        sender = data.sender;
        receiver = data.receiver
    });

    socket.on('trial-message', function(data){
        console.log(data.message);
        var li = $('<li>');
        li.text(data.message);
        li.addClass('received');
        messages.append(li);
    });

    // Message SEND Button is clicked 
    send_btn.addEventListener("click", function(event){
        event.preventDefault();

        if(msg_text.val()!=''){

            /*
            // Receiver's code
            msgArray.push(msg_text.val())
            var li = $('<li>').text(msg_text.val());
            var span = $('<span>').text('mohsinsackeer: ');
            span.addClass('sender-username');
            li.prepend(span);
            li.addClass('received');
            messages.append(li);
            */

            
            // Show the test as sent
            //msgArray.push(msg_text.val())
            var li = $('<li>');
            var msg = msg_text.val();
            li.text(msg);
            li.addClass('sent');
            messages.append(li);
            
            // Send the message and receiver's username to 
            data = {'receiver' : receiver,
                    'message'  : msg}
            socket.emit('send message', data);

            // Empty the input bar
            msg_text.val('');

            // Scroll down to the bottom of chat
            $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        }
    });

};



$(document).ready(main);