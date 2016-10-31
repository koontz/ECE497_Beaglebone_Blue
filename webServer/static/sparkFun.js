var socket;
var red=0;
var green=0;

$("#slider1").slider({min:-90, max:90, slide: function(event, ui) {
    socket.emit("servo", {index: 1, position: ui.value});
    }});
$("#slider2").slider({min:-90, max:90, slide: function(event, ui) {
    socket.emit("servo", {index: 2, position: ui.value});
    }});
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
    socket.on('read',function(data){
        var index = "#"+data.side+data.sensor +"Result";
        $(index).text(data.value);
    });
}

function disconnect(){
    socket.disconnect();
}

function toggleRed(){
    socket.emit('red',0);
}

function toggleGreen(){
    socket.emit('green',0);
}
function readLeftBumper(){
    socket.emit('read',{side: 'left',sensor: 'Bumper'});
} //TODO update leftBumpResult
function readRightBumper(){
    socket.emit('read',{side: 'right',sensor: 'Bumper'});
}
function readLeftSonic(){
    socket.emit('read',{side: 'left',sensor: 'Sonic'});
}//leftSonicResult
function readRightSonic(){
    socket.emit('read',{side: 'right',sensor: 'Sonic'});
}
function readLeftEn(){
    socket.emit('read',{side: 'left',sensor: 'En'});
} //leftEnResult
function readRightEn(){
    socket.emit('read',{side: 'right',sensor: 'En'});
}
function readLeftLine(){
    socket.emit('read',{side: 'left',sensor: 'Line'});
} //leftLineResult
function readRightLine(){
    socket.emit('read',{side: 'right',sensor: 'Line'});
}

connect();
