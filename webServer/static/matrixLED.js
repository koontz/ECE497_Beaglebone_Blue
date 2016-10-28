    var socket;
    var firstconnect = true,
        i2cNum  = "0x70",
	disp = [[],[],[],[],[],[],[],[]];

// Create a matrix of LEDs inside the <table> tags.
var matrixData;
for(var j=7; j>=0; j--) {
	matrixData += '<tr>';
	for(var i=0; i<8; i++) {
	    matrixData += '<td><div class="LED" id="id'+i+'_'+j+
		'" onclick="LEDclick('+i+','+j+')">'+
		' '+'</div></td>';
	    }
	matrixData += '</tr>';
}
$('#matrixLED').append(matrixData);

// The slider controls the overall brightness
$("#slider1").slider({min:0, max:15, slide: function(event, ui) {
	socket.emit("brightness",  {i2cNum: i2cNum, i: ui.value+0xe0});
    }});

// Send one color when LED is clicked.
function LEDclick(i, j) {
    var square = disp[i][j];
    //Changes color on display
    if(square === 3) {
        disp[i][j] = 0;
        $('#id'+i+'_'+j).removeClass('red');
    }else if(square === 2){
        disp[i][j] = 3;
        $('#id'+i+'_'+j).removeClass('orange');
        $('#id'+i+'_'+j).addClass('red');
    }else if(square === 1){
        disp[i][j] = 2;
        $('#id'+i+'_'+j).removeClass('green');
        $('#id'+i+'_'+j).addClass('orange');
    }else {
        disp[i][j] = 1;
        $('#id'+i+'_'+j).addClass('green');
    }
    //instruct server what color it is
    socket.emit('i2cset', {i2cNum: i2cNum, i: i, j: j, 
			     disp: disp[i][j]});
}

function connect() {
    if(firstconnect) {
        socket = io.connect(null);
        // See https://github.com/LearnBoost/socket.io/wiki/Exposed-events
        // for Exposed events
        socket.on('message', function(data)
            { status_update("Received: message " + data);});
        socket.on('connect', function()
            { status_update("Connected to Server"); });
        socket.on('disconnect', function()
            { status_update("Disconnected from Server"); });
        socket.on('reconnect', function()
            { status_update("Reconnected to Server"); });
        socket.on('reconnecting', function( nextRetry )
            { status_update("Reconnecting in " + nextRetry/1000 + " s"); });
        socket.on('reconnect_failed', function()
            { message("Reconnect Failed"); });

        socket.on('matrix',  matrix);
        // Read display for initial image.  Store in disp[]
        socket.emit("matrix", i2cNum);
      }else {
        connect();
      }
    }
function disconnect() {
    socket.disconnect();
}

//Converts data into the display format
function matrix(data) {
    var i, j;
	console.log(data);
	for(i=0;i<data.length;i++){
        for(j=0;j<data.length;j++){
            disp[i][j] = data[i][j];
        }
	}
    //updates the classes
    for (i = 0; i < disp.length; i++) {
        for (j = 0; j < disp.length; j++) {
            changeColor(i,j,disp[i][j])
        }
    }
}
//function to update color classes
function changeColor(i,j,val){
    $('#id' + i + '_' + j).removeClass('red');
    $('#id' + i + '_' + j).removeClass('green');
    $('#id' + i + '_' + j).removeClass('orange');
    if(val ===3){
        $('#id' + i + '_' + j).addClass('red');
    }else if(val===2){
        $('#id' + i + '_' + j).addClass('orange');
    }else if(val===1){
        $('#id' + i + '_' + j).addClass('green');
    }
}
    function status_update(txt){
	$('#status').html(txt);
    }

    function updateFromLED(){
      socket.emit("matrix", i2cNum);    
    }

connect();

$(function () {
    // setup control widget
    $("#i2cNum").val(i2cNum).change(function () {
        i2cNum = $(this).val();
    });
});
