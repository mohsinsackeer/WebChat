var main = function(){
    console.log('chat.js is active!');

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
    var msgArray =[];
    var messages = $('#messages');

    send_btn.addEventListener("click", function(event){
        event.preventDefault();

        if(msg_text.val()!=''){
            msgArray.push(msg_text.val())
            var li = $('<li>').text(msg_text.val());
            var span = $('<span>').text('mohsinsackeer: ');
            span.addClass('sender-username');
            li.prepend(span);
            li.addClass('received');
            messages.append(li);

            msgArray.push(msg_text.val())
            var li = $('<li>');
            li.text(msg_text.val());
            li.addClass('sent');
            messages.append(li);
            msg_text.val('');
        }
    });

    /*
    send.on('click',function(){
        if(msg_text.val()!=''){
            msgArray.push(msg_text.val())
            var li = $('<li>');
            li.text(msg_text.val());
            messages.append(li);
            msg_text.val('');
        }
    });
    */
};



$(document).ready(main);