$(document).ready(function() {
    loadMyProfile();
    loadOtherProfile();
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
	$("#userInfo").append('<p>'+'<b> Favorite song:' + ""+ '</b></p>');
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

function loadOtherProfile() {
    otherUser = $("#anyUser").text();    
    $.getJSON("/getOtherInfo", {otherUser:otherUser}, function(data) {
	console.log(data);
	$("#anyUser").empty();
	$('#ytapiplayer2').empty();
	$("#anyUser").append('<p>'+'<b> Name: </b>'+data[0]+'</p>');
	$("#anyUser").append('<p>'+'<b> Hobbies: </b>'+data[1]+'</p>');
	$("#anyUser").append('<p>'+'<b> Gender: </b>'+data[2]+'</p>');
	$("#anyUser").append('<p>'+'<b> Age: </b>'+data[3]+'</p>');
	$("#anyUser").append('<p>'+'<b> Favorite song: </b>' + "" + '</p>');
	});
    $.getJSON("/getsongother", {otherUser:otherUser}, function(data) {
	console.log(data);
	var params = { allowScriptAccess: "always" };
	var atts = { id: "myytplayer1" };
	$("#myytplayer1").attr('data', "http://www.youtube.com/v/" + data[0] + "?enablejsapi=1&playerapiid=ytplayer&version=3");
	var url = "http://www.youtube.com/v/" + data[0] + "?enablejsapi=1&playerapiid=ytplayer&version=3";
	swfobject.embedSWF(url,"ytapiplayer2","425", "356", "8", null, null, params, atts);
    });
}