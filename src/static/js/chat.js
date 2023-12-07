var main = function(){
    console.log('chat.js is active!');

    var socket = io();
    var receiver;
    var sender;
    var all_usernames = [];
    // var cloudinary = require('cloudinary').v2;
    var error_title, error_message;


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
    var test_bt = document.getElementById('test-bt');

    var modal = document.getElementById('image-modal');

    var modalClose = document.getElementById('image-modal-close');
    modalClose.addEventListener('click', function() { 
        modal.style.display = "none";
    });

    // global handler
    document.addEventListener('click', function (e) { 
    if (e.target.className.indexOf('image-modal-target') !== -1) {
        var img = e.target;
        var modalImg = document.getElementById("image-modal-content");
        // var captionText = document.getElementById("image-modal-caption");
        modal.style.display = "block";
        modalImg.src = img.src;
        // captionText.innerHTML = img.alt;
    }
    });


    var display_load_older_messages_btn = function(type, username, chunk_num){
        var li = $('<li>');
        li.append("<a href='#' id='loadOlder'>Load Older Messages</a>");
        messages.append(li);

        $("#loadOlder").on("click", function(){
            data = {
                'type'              : type,
                'name_or_username'  : username,
                'chunk_num'         : chunk_num+1
            };
            socket.emit('req-list-of-messages', data);
        });
    }

    var display_load_newer_messages_btn = function(type, username, chunk_num){
        var li = $('<li>');
        li.append("<a href='#' id='loadNewer' data-chunk" + chunk_num + ">Load Newer Messages</a>");
        messages.append(li);

        $('#loadNewer').on('click', function(){
            data = {
                'type'              : type,
                'name_or_username'  : username,
                'chunk_num'         : chunk_num-1
            };
            socket.emit('req-list-of-messages', data);
        });
    }

    var display_message = function(message, class_name, is_image){
        msg = {
            'message': message,
            'class': class_name,
            'is_image': is_image
        };
        if(!is_image){
            var li = $('<li>');
            li.append('<div class = div-'+ class_name +'> <p >'+ message +'</p> </div>');
            li.addClass(class_name);
            messages.append(li);
        }else{
            var li = $('<li>');
            li.append(`<div class = div-${class_name} > <img class="image-modal-target" src=${message}></img> </div> `);
            li.addClass(class_name);
            messages.append(li);

        }
        // else{
        //     var li = $('<li>');
        //     li.append('<div class = div-'+ class_name +'> <p >to be come</p> </div>');
        //     li.addClass(class_name);
        //     messages.append(li);
        // }

    }

    socket.on("set-username", function(data){
        sender = data.sender;
        console.log(sender);

        // $(".btn.btn-danger").text(sender);
        $("#contacts-section > div.contacts-header > span").text(sender);
        $("#contacts-section > div.contacts-header > div.image-holder").append('<div class = demo-image><img src = "'+data.dp_url+'"  alt="contact_image"></div>')
        $(".btn-group").show();
    })

    // hide serarch tab
    $("#search-button").on('click', function(){
        console.log("Search Button Clicked!");
        if($("#div-search-username").css("display") != "none"){
            $("#div-search-username").css("display","none");
        }else{
            $("#div-search-username").css("display","block");
        }
    })

    var insertContact = function(contact){
        if (contact.type === 'user'){
            if (all_usernames.includes(contact.username))
            {
                return;
            }
            else{
                all_usernames.push(contact.username);
            }
        }
        var li = $('<li>');
        var div = $('<div>');
        div.addClass("contacts-listitem");
        div.prepend('<div class = demo-image><img src = "'+contact.dp_url+'"  alt="contact_image"></div>'); //to be changed later
        div.append('<span>'+ contact.name +'</span>');
        li.append(div);
        li.addClass(contact.username);
        list.append(li);
        var class_selector = '.' + contact.username.split(' ').join('.');
        $("#chat-list").on('click', 'li'+ class_selector, function(){
            console.log(2);
            console.log(contact.username);
            
            $(".div-chat-name span").text(contact.name);
            $(".div-chat-name div").empty();
            $(".div-chat-name div").addClass("demo-image");
            $(".div-chat-name div").append('<img src = "'+contact.dp_url+'"  alt="contact_image">');
            // $(".div-chat-name img").attr("src", str);
            // $(".div-chat-name img").attr("alt", "friend's profile image");
            // $(".div-chat-name img").addClass("profile-pic");
            $('.messages').empty();
            receiver = {'type': contact.type,
                        'name_or_username': contact.username,
                        'chunk_num': 1};
            console.log('holaaaa');
            console.log(receiver);

            socket.emit('req-list-of-messages', receiver);
        });
    };

    // Display the name of all users in the contacts section
    socket.on("get-list-of-contacts", function(list_of_users){
        console.log("Receieved List of Chats!")
        var list = $('#chat-list');
        list.empty();
        var str = "";
        
        list_of_users.forEach(function(user){
            insertContact(user);
        });
    });

    $(window).on('beforeunload', function(event){
        //event.preventDefault();
        //return event.returnValue = 'Are you sure you want to exit?'
    });

    socket.on('connect', function(){
        console.log('connect');
        $(".contacts-p").text("Contacts Section");
        socket.emit('req-list-of-contacts', 'request');
    });

    socket.on('disconnect', function(){
        $(".btn-group").hide();
        $(".contacts-p").show();
        location.reload(true);
        console.log('Reloaded');
    });

    socket.on('get-list-of-messages', function(list_of_messages){
        console.log('get-list-of-messages');
        $('.messages').empty();
        list_of_messages.forEach(function(msg){
            if (msg.hasOwnProperty('load_button_type')){
                if (msg.load_button_type == 'older'){
                    display_load_older_messages_btn(msg.type, msg.name_or_username, msg.chunk_num);
                } else{
                    display_load_newer_messages_btn(msg.type, msg.name_or_username, msg.chunk_num);
                }
                return;
            }
            if (msg.from == sender){
                display_message(msg.text, 'sent', msg.is_image);
            } else {
                display_message(msg.text, 'received', msg.is_image);
            }
        });
        // $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        $('.div-chat-window').scrollTop($('.div-chat-window')[0].scrollHeight);
        // console.log($('.div-chat-window')[0].scrollHeight);
    });

    socket.on('display-message', function(data){

        if (data.from !== receiver.name_or_username) { return; }
        console.log(data.text);
        // var li = $('<li>');
        // li.append('<div class = div-received> <p >'+ data.message +'</p> </div>');
        // li.addClass('received');
        // messages.append(li);

        display_message(data.text, 'received', data.is_image);
        
    });

    // Message SEND Button is clicked 
    send_btn.addEventListener("click", function(event){
        event.preventDefault();

        if(msg_text.val()!=''){
            var msg = msg_text.val();
            display_message(msg, 'sent', false);
            // var file = document.getElementById("upload").files[0];
            
            // Send the message and receiver's username to 
            data = {
                'type': receiver.type,
                'receiver': receiver.name_or_username, 
                'is_image':0,
                'message': msg}
            console.log(data);
            socket.emit('send-message', data);

            // Empty the input bar
            msg_text.val('');

            // Scroll down to the bottom of chat
            $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        }
    });

    test_bt.addEventListener('click',(event)=>{
        event.preventDefault()
        console.log("img sent initialized")
        var file = document.getElementById("upload").files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
            // var msg_data = reader.result;
            var base64data = reader.result;
            data = {
                'type': receiver.type,
                'receiver' : receiver.name_or_username,
                'is_image': true,
                'message' : base64data
            }
            console.log(base64data);
            socket.emit('send-message', data);
            display_message(base64data, 'sent',true);
          }
        // reader.onload = function() {};
        
    });



    socket.on('answerToDoesUsernameExists', function(data){
        if (data['answer'] === 'True'){
            // do something
            console.log(data);
            user = {'type': 'user',
                    'username': data.username,
                    'name': data.name,
                    'dp_url': data.dp_url};
            insertContact(user);
        }
    });

    socket.on('group-created', function(data){
        socket.emit('req-list-of-contacts', 'Request');
    });

    socket.on('warning-or-error', function(data){
        error_title = data.warning_or_error
        error_message = data.message
        // $("#errorWarningModal #modalTitle").text(title);
        // $("#errorWarningModal #modalText").text(message);
        // $("#errorWarningModal").modal('toggle');
        // console.log($("#errorWarningModal #modalTitle").text());
        // console.log($("#errorWarningModal #modalText").text());
        alert(error_title + '\n' + error_message);
        error_title = '';
        error_message = '';
    });

    $('#search-username').on("keypress", function(event){
        if ((event.keyCode === 13) && ($('#search-username').val() !== sender)){
            // console.log($('#search-username').val());
            socket.emit('doesUsernameExists', {'username': $('#search-username').val()})
            // var username = $('#search-username').val();
            // $('#chat-list li.'+ username).trigger('click');
        }
    });

    // To open the modal box
    $("#anchorTagCreateGroup").on('click', function(){
        // $("#createGroupModal").show();
        console.log($("#createGroupModal #fillAllEntryMessage").text(''));
        $("#createGroupModal").modal('toggle');
    });

    $("#createGroupButton").on('click', function(){
        var nameInput = $("#groupNameInput"),
            membersInput = $("#groupMembersInput"),
            adminsInput = $("#groupAdminsInput");
        
        var group_name = nameInput.val(),
            group_members = membersInput.val(),
            group_admins = adminsInput.val();

        if ((group_name!=='') && (group_members!=='') && (group_admins!=='')){
            // console.log(group_name);
            // console.log(group_members);
            // console.log(group_admins);
            nameInput.val('');
            membersInput.val('');
            adminsInput.val('');
            data_to_send = {
                'name': group_name,
                'members': group_members,
                'admins': group_admins
            }
            console.log(data_to_send);
            socket.emit('create-new-group', data_to_send);
            $("#createGroupModal").modal('toggle');
        }
        else{
            console.log($("#createGroupModal #fillAllEntryMessage").text('You must fill all entries!'));
        }

    });
};



$(document).ready(main);