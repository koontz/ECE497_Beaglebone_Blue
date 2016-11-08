var matrixData;
for(var j=128; j>=0; j--) {
	matrixData += '<tr>';
	for(var i=0; i<128; i++) {
	    matrixData += '<td><div class="camcell" id="id'+i+'_'+j+
		'" >'+' '+'</div></td>';
	    }
	matrixData += '</tr>';
}
$('#camMatrix').append(matrixData);