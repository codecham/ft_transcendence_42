'use strict';

// var backendUrl = "http://localhost:8080/api";
var backendUrl = "https://localhost:8443/api";
var socketUrl = "ws://localhost:8443/ws";
var connected_user = "";

(function () {
    function init() {
        var router = new Router([
            new Route('home', 'home/home.html', ["home/home.css"], ["home/home.js"], true),
            new Route('lobby', 'lobby/lobby.html', ['lobby/lobby.css'], ["lobby/lobby.js"]),
            new Route('room', 'room/room.html', ["room/room.css"], ["room/pong.js", "room/room.js" ,"room/style.js", "room/request.js"]),
            new Route('sign-up', 'auth/signUp/signUp.html', ['auth/signUp/signUp.css'], ['auth/signUp/signUp.js']),
            new Route('sign-in', 'auth/signIn/signIn.html', ['auth/signIn/signIn.css'], ['auth/signIn/signIn.js']),
            new Route('profile', 'profile/profile.html', ['profile/profile.css'], ['profile/profile.js']),
            new Route('edit-profile', 'profile/edit-profile.html', ['profile/edit-profile.css'], ['profile/edit-profile.js']),
            new Route('tournament', 'room/tournament.html', ['room/tournament.css'], ['room/tournament.js']),
        ]);
    }
    init();
}());
