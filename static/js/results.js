$(document).ready(function() {
  loadNames();
});

var surveyname;

function loadNames() {
    $.getJSON("/getnames", function(data){
	$("#names").empty();
	if (data.length > 0) {
            for (var i = -1; i < data.length; i++){
		if (i == -1) {
		    $("#names").append('<option value="'+000+'">' + "Select a survey to see the results:" + '<\p>');
		}
		else {
		    //check if user answered
		    var item=$('<option value="'+data[i]+'">'+ data[i]+'</option>');
		    $("#names").append(item);
		}
            }
	}
	else {
	    console.log("nope");
	    $("#matches").append("<b>" + "NO SURVEYS FOUND" + "</b>");
	}
	$("#names").change(loadMatches);  
    });
}



function loadMatches(e) {
    surveyname = $(this).attr("value");
    $("#matches").empty();
    $.getJSON("/matchfind", {surveyname: surveyname}, function(data){
	$("#matches").append("</br>");
	$("#matches").append("<b>" + "BEST: </b> ");
	for (var i=0; i <data[2].length; i++) {
	    $("#matches").append(data[2][i] + " profile: <a href='../profile/" + data[2][i] +"'> link to profile "+ "</a>" );
	}
	$("#matches").append("<b>" + "WORST: </b> ");
	for (var i=0; i <data[3].length; i++) {
	    $("#matches").append(data[2][i] + " profile: <a href='ml7.stuycs.org:6565/profile/" + data[2][i]+ "'>link to profile" + "</a>" );
	}
	//data is matches
    });
}
