var socket;
var red=0;
var green=0;

$("#slider1").slider({min:0, max:15, slide: function(event, ui) {
    socket.emit("servo", {index: 1, position: ui.value});
    }});
function toggleRed(){
    socket.emit('red',0);
}

function toggleGreen(){
    socket.emit('green',0);
}
function status_update(txt){
    $('#status').html(txt)
}

function connect(){
    socket = io.connect(null);
    socket.on('message',function(data){
        status_update("Received: message "+data);
    });
    socket.on('connect', function(){
        status_update("Connected to Server");
    });
    socket.on('disconnect', function(){
        status_update("Disconnected to Server");
    });
/*
    socket.on('reconnect', function(){
        status_update("Reconnected to Server");
    });
I dont think we care about reconnecting right now
*/
    socket.on('red',function(data){
        red = data;
    });
    socket.on('green',function(data){
        green = data;
    });
}

function disconnect(){
    socket.disconnect();
}
connect();
