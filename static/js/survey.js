var surveyname;

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
    
    surveyname = $(this).attr("value");
    var prefs = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"];
    
    $("#survey").empty();
    $("#survey").append('</br>');
    $.getJSON("/getquestions", {surveyname: surveyname}, function(data){
	for (var i = 0; i < data.length; i++){
	    $("#survey").append('<p>' + (i+1) + '. ' + data[i][0] + '</p>');
	    if (data[i][1] == 'number'){
		for (var j = 0; j < 5; j++){
		    if (j == 0)
			$("#survey").append('<input type="radio" name="'+i+'" value="'+j+'" checked="checked">'+j+'   '+'</input>');
		    else
			$("#survey").append('<input type="radio" name="'+i+'" value="'+j+'">'+j+'   '+'</input>');
		}
	    }
	    else{
		for (var j = 0; j < 5; j++){
		    if (j == 0)
			$("#survey").append('<input type="radio" name="'+i+'" value="'+j+'" checked="checked">'+prefs[j]+'   '+'</input>');
		    else
			$("#survey").append('<input type="radio" name="'+i+'" value="'+j+'">'+prefs[j]+'   '+'</input>');
		}
	    }
	    $("#survey").append('</br></br>');
	    if (i == data.length - 1){
		$("#survey").append('<button id="submitSurvey" name="Submit" type="submit" value="Submit">Submit</button>');
		$("#submitSurvey").click(submitSurvey);
	    }
	}	
    });
}

function submitSurvey(){
    var responses = []
    for (var i=0; i<$("input").length / 5; i++) {
	responses.push( $('input[type="radio"][name='+i+']:checked').attr('value') );
	
    }
    var responseString = responses.join(",");
    $.getJSON("/submitSurvey", {surveyname:surveyname, ans:responseString}, function(data){});1
    
}





function loadMatches(surveyname, username) {
    $.getJSON("/matchfind", {surveyname: surveyname, username: username}, function(data){
	//data is matches
    });
}

