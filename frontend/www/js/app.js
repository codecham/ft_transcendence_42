var backendUrl = '';
var g_socketsUrl = '';
var connected_user = '';


async function getHostIpAddress()
{
    try {
        const response = await fetch('host_ip.json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('Error fetching IP address:', error);
        return null;
    }
}


(function () {
    async function init() {
        const reponse = await getHostIpAddress();
        backendUrl = `https://${reponse}:8443/api`;
        g_socketsUrl = `wss://${reponse}:8001/ws/game/`;
        var router = new Router([
            new Route('home', 'home/home.html', ["home/home.css"], ["home/home.js"], true),
            new Route('lobby', 'lobby/lobby.html', ['lobby/lobby.css'], ["lobby/lobby.js"]),
            new Route('room', 'room/room.html', ["room/room.css"], ["room/pong.js", "room/room.js" ,"room/style.js", "room/request.js"]),
            new Route('sign-up', 'auth/signUp/signUp.html', ['auth/signUp/signUp.css'], ['auth/signUp/signUp.js']),
            new Route('sign-in', 'auth/signIn/signIn.html', ['auth/signIn/signIn.css'], ['auth/signIn/signIn.js']),
            new Route('profile', 'profile/profile.html', ['profile/profile.css'], ['profile/profile.js']),
            new Route('friends', 'friends/friends.html', ['friends/friends.css'], ['friends/friends.js']),
            new Route('edit-profile', 'profile/edit-profile.html', ['profile/edit-profile.css'], ['profile/edit-profile.js']),
            new Route('tournament', 'room/tournament.html', ['room/tournament.css'], ['room/tournament.js']),
            new Route('other_profile', 'profile/other_user_profile.html', ['profile/other_user_profile.css'], ['profile/other_user_profile.js']),
        ]);
    }
    init();
}());
