$(document).ready(function() {
    loadMyProfile();
    loadOtherProfile();
})

function loadMyProfile() {
    $("#userInfo").empty();
    $.getJSON("/getUserInfo", function(data) {
	console.log(data);
	$("#userInfo").append('<p>'+'<b> Name: </b>'+data[0]+'</p>');
	$("#userInfo").append('<p>'+'<b> Hobbies: </b>'+data[1]+'</p>');
	$("#userInfo").append('<p>'+'<b> Gender: </b>'+data[2]+'</p>');
	$("#userInfo").append('<p>'+'<b> Age: </b>'+data[3]+'</p>');
    }); 
}

function loadOtherProfile() {
    otherUser = $("#anyUser").text();
    
    $.getJSON("/getOtherInfo", {otherUser:otherUser}, function(data) {
	console.log(data);
	$("#anyUser").empty();
	$("#anyUser").append('<p>'+'<b> Name: </b>'+data[0]+'</p>');
	$("#anyUser").append('<p>'+'<b> Hobbies: </b>'+data[1]+'</p>');
	$("#anyUser").append('<p>'+'<b> Gender: </b>'+data[2]+'</p>');
	$("#anyUser").append('<p>'+'<b> Age: </b>'+data[3]+'</p>');
    });
}