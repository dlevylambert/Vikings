$(document).ready(function() {
    loadProfile();
})

function loadProfile() {
    $("#userInfo").empty();
    $.getJSON("/getUserInfo", function(data) {
	console.log(data);
	$("#userInfo").append('<p>'+data[0]+'</p>');
	$("#userInfo").append('<p>'+data[1]+'</p>');
	$("#userInfo").append('<p>'+data[2]+'</p>');
	$("#userInfo").append('<p>'+data[3]+'</p>');
    }); 
}