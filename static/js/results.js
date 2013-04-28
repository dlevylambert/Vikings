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
      var item=$('<option value="'+data[i]+'">'+ data[i]+'</option>');
      $("#names").append(item);
    }
            }
}
else {
console.log("nope");
$("#matches").append("<b>" + "NO SERVEYS FOUND" + "</b>");
}
$("#names").change(loadMatches);  
    });
}



function loadMatches(e) {
    surveyname = e.attr("value");
    $.getJSON("/matchfind", {surveyname: surveyname}, function(data){
        $("#matches").append("<b>" + "BEST: " + data['best'] + "<br>" + "WORST: " + data['worst'] + "</br></b>);
//data is matches
    });
}
