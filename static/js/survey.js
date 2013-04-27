$(document).ready(function(){
    loadNames();
});

function loadNames() {
    $.getJSON("/getnames", function(data){
	$("#names").empty();
	for (var i = 0; i< data.length; i++){
	    var item=$('<option value="'+data[i]+'">'+ data[i]+'</option>');
	    $("#names").append(item);
	}
    });
}
	     