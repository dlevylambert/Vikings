$(document).ready(function(){
    loadNames();
});

function loadNames() {
    $.getJSON("/getnames", function(data){
	$("#names").empty();

	if (data.length) > 0 {
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
	$("#names").change(loadInfo);
	$("#names").change(loadQuestions);
    });
}
	     

function loadInfo(e) {
    /* put survey questions and radio buttons in #survey*/
    var surveyquestions = loadQuestions($(this).attr("value")); //surveyquestions is a list of lists. format: [[question, type], [questions, type]]
}

function loadQuestions(surveyname) {
    var q = []
    $.getJSON("/getquestions", {surveyname: surveyname}, function(data)) {
	for (var i = 0; i<data.length; i++) {
	    q[i] = data["questions"][i];
	}
    }
    return q;
	//variable data now represents the questions of a particular survey. returns from util.py getSurveyQs, which is all the info for a survey
    }
}

function loadMatches(surveyname, username) {
    $.getJSON("/matchfind", {surveyname: surveyname, username: username}, function(data)) {
	//data is matches
    }
}
