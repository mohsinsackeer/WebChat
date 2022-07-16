
var main = function(){
    console.log('chat.js is active!');

    var socket = io();
    var receiver = "";
    var sender;
    var all_usernames = [];


    var names= ["Adwaith", "Mohsin","DK"];
    var list = $('#chat-list');
    var str = "https://png.pngitem.com/pimgs/s/150-1503945_transparent-user-png-default-user-image-png-png.png"
    names.forEach((i)=>{
        var li = $('<li>');
        var div = $('<div>');
        div.addClass("check_class");
        div.prepend('<img src = "'+str+'"  alt="contact_image">');
        div.append('<span >'+ i +'</span>');
        li.append(div);
        list.append(li);
    });

    var send_btn = document.getElementById('send_bt');
    var msg_text =$('#msg_input');
    var messages = $('#messages');

    socket.on("set-username", function(data){
        sender = data.sender;
    });

    // Display the name of all users in the contacts section
    socket.on("get-list-of-users", function(list_of_users){

        var list = $('#chat-list');
        list.empty();
        var str = "";
        
        list_of_users.forEach(function(user){
            all_usernames.push(user.username);
            if (user.username === sender){ return; }

                var li = $('<li>');
                var div = $('<div>');
                div.addClass("contacts-listitem");
                div.prepend('<div class = demo-image></div>'); //to be changed later
                div.append('<span >'+ user.name +'</span>');
                li.append(div);
                li.addClass(user.username);
                list.append(li);

                $("#chat-list").on('click', 'li.'+user.username, function(){
                    console.log(user.username);

                    $(".div-chat-name span").text(user.name);
                    $(".div-chat-name div").addClass("demo-image");
                    // $(".div-chat-name img").attr("src", str);
                    // $(".div-chat-name img").attr("alt", "friend's profile image");
                    // $(".div-chat-name img").addClass("profile-pic");
                    $('.messages').empty();
                    receiver = user.username;
                });
            
        });
    });

    socket.on('display-message', function(data){

        if (data.from !== receiver) { return; }
        console.log(data.message);
        var li = $('<li>');
        li.append('<div class = div-received> <p >'+ data.message +'</p> </div>');
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
            li.append('<div class = div-sent> <p >'+ msg +'</p> </div>');
            li.addClass('sent');
            messages.append(li);
            
            // Send the message and receiver's username to 
            data = {'receiver' : receiver,
                    'message'  : msg}
            socket.emit('send-message', data);

            // Empty the input bar
            msg_text.val('');

            // Scroll down to the bottom of chat
            $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        }
    });

    $('#search-username').on("keypress", function(event){
        if (event.keyCode === 13){
            var username = $('#search-username').val();
            $('#chat-list li.'+ username).trigger('click');
        }
    });
};



$(document).ready(main);