$(document).ready(function() {
    loadMyProfile();
})

function loadMyProfile() {
    $("#userInfo").empty();
    $('#ytapiplayer1').empty();
    $.getJSON("/getUserInfo", function(data) {
	console.log(data);
	$("#userInfo").append('<p>'+'<b> Name: </b>'+ data[0]+'</p>');
	$("#userInfo").append('<p>'+'<b> Hobbies: </b>'+data[1]+'</p>');
	$("#userInfo").append('<p>'+'<b> Gender: </b>'+data[2]+'</p>');
	$("#userInfo").append('<p>'+'<b> Age: </b>'+data[3]+'</p>');
	$("#userInfo").append('<p>'+'<b> Favorite song: </b></p>');
    });
    $.getJSON("/getsong", function(data) {
	console.log(data);
	var params = { allowScriptAccess: "always" };
	var atts = { id: "myytplayer" };
	$("#myytplayer").attr('data', "http://www.youtube.com/v/" + data[0] + "?enablejsapi=1&playerapiid=ytplayer&version=3");
	var url = "http://www.youtube.com/v/" + data[0] + "?enablejsapi=1&playerapiid=ytplayer&version=3";
	swfobject.embedSWF(url,"ytapiplayer1","425", "356", "8", null, null, params, atts);
    }); 
}