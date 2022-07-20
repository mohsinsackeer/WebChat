
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

    var display_message = function(message, class_name){
        var li = $('<li>');
        li.append('<div class = div-'+ class_name +'> <p >'+ message +'</p> </div>');
        li.addClass(class_name);
        messages.append(li);
    };

    socket.on("set-username", function(data){
        sender = data.sender;
    });

    var insertContact = function(user){
        if (all_usernames.includes(user.username)){return;}
        all_usernames.push(user.username);
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

            socket.emit('req-list-of-messages', receiver);
        });
    };

    // Display the name of all users in the contacts section
    socket.on("get-list-of-users", function(list_of_users){

        var list = $('#chat-list');
        list.empty();
        var str = "";
        
        list_of_users.forEach(function(user){
            insertContact(user);
        });
    });

    $(window).on('beforeunload', function(event){
        event.preventDefault();
        return event.returnValue = 'Are you sure you want to exit?'
    });

    socket.on('connect', function(){
        $(".contacts-p").text("Contacts Section");
    });

    socket.on('disconnect', function(){
        $(".contacts-p").text("DISCONNECTED...");
        location.reload(True);
        console.log('Reloaded');
    });

    socket.on('get-list-of-messages', function(list_of_messages){
        console.log('get-list-of-messages')
        list_of_messages.forEach(function(msg){
            display_message(msg.message, msg.class_name);
        });
        $("html, body").animate({ scrollTop: $(document).height() }, 1000);
    });

    socket.on('display-message', function(data){

        if (data.from !== receiver) { return; }
        console.log(data.message);
        // var li = $('<li>');
        // li.append('<div class = div-received> <p >'+ data.message +'</p> </div>');
        // li.addClass('received');
        // messages.append(li);

        display_message(data.message, 'received');
    });

    // Message SEND Button is clicked 
    send_btn.addEventListener("click", function(event){
        event.preventDefault();

        if(msg_text.val()!=''){

            var msg = msg_text.val();
            display_message(msg, 'sent')
            
            // Send the message and receiver's username to 
            data = {'receiver': receiver, 'message': msg}
            socket.emit('send-message', data);

            // Empty the input bar
            msg_text.val('');

            // Scroll down to the bottom of chat
            $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        }
    });

    socket.on('answerToDoesUsernameExists', function(data){
        if (data['answer'] === 'True'){
            // do something
            console.log(data);
            user = {'username': data.username,
                    'name': data.name};
            insertContact(user);
        }
    });

    $('#search-username').on("keypress", function(event){
        if ((event.keyCode === 13) && ($('#search-username').val() !== sender)){
            // console.log($('#search-username').val());
            socket.emit('doesUsernameExists', {'username': $('#search-username').val()})
            // var username = $('#search-username').val();
            // $('#chat-list li.'+ username).trigger('click');
        }
    });
};



$(document).ready(main);