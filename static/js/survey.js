$(document).ready(function(){
    loadNames();
});

function loadNames() {
    $.getJSON("/getnames", function(data){
	$("#names").empty();

	if (data.length > 0) {
            for (var i = -1; i < data.length; i++){
		if (i == -1) {
		    $("#names").append('<option value="'+000+'">' + "Select a survey to take it:" + '<\p>');
		}
		else {
		    var item=$('<option value="'+data[i]+'">'+ data[i]+'</option>');
		    $("#names").append(item);
		}
            }
	}
	else {
	    console.log("nope");
	    $("#survey").append("<b>" + "NO MOVIES FOUND! GO BACK TO SEARCH AGAIN" + "</b>");
	}
	$("#names").change(loadQuestions);	
    });
}
	     

function loadQuestions(e) {
    /* put survey questions and radio buttons in #survey*/
    $("#survey").empty();
    $("#survey").append('</br>');
    $.getJSON("/getquestions", {surveyname: $(this).attr("value")}, function(data){
	for (var i = 0; i < data.length; i++){
	    $("#survey").append('<p>' + (i+1) + '. ' + data[i][0] + '</p>');
	    for (var j = 0; j < 5; j++){
		if (j == 0)
		    $("#survey").append('<input type="radio" name="'+i+'" value="'+j+'" checked="checked">'+j+'</input>');
		else
		    $("#survey").append('<input type="radio" name="'+i+'" value="'+j+'">'+j+'</input>');
	    }
	    $("#survey").append('</br></br>');
	    if (i == data.length - 1)
		$("#survey").append('<input class="button" id="submitSurvey" type="submit" name="submitSurvey" value="Submit"></input>');
	}	
    });
}

function loadMatches(surveyname, username) {
    $.getJSON("/matchfind", {surveyname: surveyname, username: username}, function(data){
	//data is matches
    });
}
