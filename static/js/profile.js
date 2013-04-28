$(document).ready(function() {
    loadProfile();
});

function loadProfile() {
    $.getJSON("/getUserInfo", function(data) {
//need to load all of that data in soon	
    });
}