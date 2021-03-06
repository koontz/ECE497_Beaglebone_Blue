var socket;
var red=0;
var green=0;

$("#slider1").slider({min:-90, max:90, slide: function(event, ui) {
    socket.emit("servo", {index: 1, position: ui.value/90});
    }});
$("#slider2").slider({min:-90, max:90, slide: function(event, ui) {
    socket.emit("servo", {index: 2, position: ui.value/90});
    }});
$("#slider3").slider({min:0, max:50, slide: function(event, ui) {
    socket.emit("throttle", ui.value/50);
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
    socket.on('sendPosition',function(data){
        $( ".camcell" ).removeClass( "blue" );
        console.log("recv"+data.x);
        $('#id'+Math.round((data.x/319)*32)+'_'+Math.round((data.y/199)*32)).addClass("blue");
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
function readCamPosition(){
    socket.emit('getPosition',0);
}
function followBall(){
    socket.emit('followBall',0);
}
function stopBall(){
    socket.emit('stopBall',0);
}

connect();
readCamPosition();
setInterval(readCamPosition, 500);
document.addEventListener('keydown', function(event) {
    if(event.keyCode == 37) {
        socket.emit('move','left');
        console.log('left');
    }else if(event.keyCode == 38) {
        socket.emit('move','up');
        console.log('up');
    }else if(event.keyCode == 40) {
        socket.emit('move','down');
        console.log('down');
    }else if(event.keyCode == 39) {
        socket.emit('move','right');
        console.log('right');
    }
});
