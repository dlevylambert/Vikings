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


//Not really sure why all these percentages are the same. Dina and Helen should investigate the algorithm because something strange seems to be going on here.

function loadMatches(e) {
    surveyname = $(this).attr("value");
    $("#matches").empty();
    $.getJSON("/matchfind", {surveyname: surveyname}, function(data){
	$("#matches").append("<b>" + "BEST: </b>");
	$("#matches").append("<table class='table-striped'>");
	$("#matches").append("<thead> <tr> <th>Name</th><th>Profile</th><th>Match %</th> </tr></thead><tbody>")
	for (var i=0; i <data[2].length; i++) {
	    
	    $("#matches").append("<tr><td>" + data[2][i] + "</td> <td> <a href='../profile/" + data[2][i] +"'> Go to Profile "+ "</a></td><td>" + data[0] + "</td></tr>");
	    console.log(data[0]);
	    
	}
	$("#matches").append("</tbody></table>");
	$("#matches").append("<b>" + "WORST: </b> ");
	$("#matches").append("<table class='table-striped'>");
	$("#matches").append("<thead> <tr> <th>Name</th><th>Profile</th><th>Match %</th> </tr></thead><tbody>")
	for (var i=0; i <data[3].length; i++) {
	    $("#matches").append("<tr><td>" + data[3][i] + "</td> <td> <a href='../profile/" + data[2][i] +"'> Go to Profile "+ "</a></td><td>" + data[1] + "</td></tr>");    
	}
	$("#matches").append("</tbody></table>");
	$("#matches").append("<b>" + "OVERALL BEST: </b> ");
	$("#matches").append("<table>");
	for (var i=0; i < 1; i++) {
	    $("#matches").append("<tr><td>" + data[4][i] + "</td> <td> <a href='../profile/" + data[2][i] +"'> Go to Profile "+ "</a></td><td>Match %:" + data[5][i] + "</td></tr>");    
	    

	}
	$("#matches").append("</table>");
	//data is matches
    });
}
