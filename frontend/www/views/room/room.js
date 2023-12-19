import { dessinerPong } from "./pong.js";

let player = {};
const start_btn_div = document.getElementById("start_button_div")
const start_btn = document.getElementById("start_btn_id")
const lobby_div = document.getElementById("lobby-div")
const pongCanvas = document.getElementById("pongDiv")
let socket;

start_btn.addEventListener('click', sendStartGame)

function sendSocket(type, data) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: type,
            data: data,
        }));
    } else {
        console.error('WebSocket connection is not open.');
    }
}


function sendStartGame() {
    console.log("Button start game pressed");
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "action",
            data: "startGame",
        }));
    } else {
        console.error('WebSocket connection is not open.');
    }
    var exempleData = {
        p1_y: 0,
        p2_y: 0,
        ball_x: 0,
        ball_y: 0
      };
}


function gameStart() {
    lobby_div.style.display = "none";
    pongCanvas.style.display = "block";
}


function setPLayerObject(player, data) {
    console.log("Data in set player: " + data);
    player.name = data.name;
    player.slot = data.slot;
    player.is_master = data.is_master;
    console.log("Player set:")
    console.log("Name: " + player.name)
    console.log("Slot: " + player.slot)
    console.log("Is_master: " + player.is_master)
}

function updatePlayerName(name) {
    const usernameElem = document.getElementById("username-btn");

    usernameElem.innerHTML = '';
	usernameElem.innerHTML = name;


}

function updateUsersList(usersList, maxPlayer) {
    const playerList = document.getElementById("player-list-settings");
    let nbPlayer = 0;
    playerList.innerHTML = "";

    for (let i = 1; i <= maxPlayer; i++) {
        const listItem = document.createElement("li");

        listItem.textContent = `Player ${i}: `;

        const spanElement = document.createElement("span");

        spanElement.id = `value_player_${i}`;
        spanElement.innerHTML = "waiting player...";
        spanElement.style.fontSize = "14px";
        spanElement.style.color = "gray";
        listItem.appendChild(spanElement);
        playerList.appendChild(listItem);
    }
    
    usersList.forEach(user => {
        const spanId = `value_player_${user.slot}`;
        const spanElement = document.getElementById(spanId);

        spanElement.innerText = "";
        spanElement.innerText = user.name;
        spanElement.style.fontSize = "17px";
        spanElement.style.color = "#188034";
        nbPlayer++;
    });

    const nbPlayerElem = document.getElementById("nb_player_button");
    nbPlayerElem.innerText = "";
    nbPlayerElem.innerText = nbPlayer;
    
}

function showError(error) {
    const errorMessageElement = document.getElementById('error-message');

    errorMessageElement.innerHTML = 'Error: ';
    errorMessageElement.innerHTML = error;
}


function getRoomId() {
    var url = window.location.href;
    var paramsString = url.split('?')[1];

    if (paramsString) {
        var paramsArray = paramsString.split('&');
        var paramsObject = {};

        paramsArray.forEach(function (param) {
            var keyValue = param.split('=');
            var key = decodeURIComponent(keyValue[0]);
            var value = decodeURIComponent(keyValue[1]);
            paramsObject[key] = value;
        });
        var room_id = paramsObject['room_id'];
	
        if (room_id !== "undefined") {
            return(room_id);
        } else {
            showError('room_id value not found on the url');
            return(undefined);
        }
    } else {
		showError('room_id value not found on the url');
        return(undefined)
    }
}

document.addEventListener('DOMContentLoaded', function() {
	const room_id = getRoomId();

    if (room_id !== undefined) {
        const socketUrl = `ws://localhost:8000/ws/game/${room_id}/`
        console.log("url socket: ", socketUrl);
        socket = new WebSocket(socketUrl);

        /*
            Open socket listening
        */
        socket.addEventListener('open', (event) => {
            console.log('WebSocket connection established:', event);
        });


        /*
            Message handler listening
        */
        socket.addEventListener('message', (event) => {
            console.log('WebSocket message received:', event);
        
            const data = JSON.parse(event.data);
            if (data.error) {
                showError(data.error);
                socket.close();
            } else {
                handleMessage(data);
            }
        });


        /*
            Errors sockets listening
        */
        socket.addEventListener('error', (event) => {
            console.error('WebSocket error:', event);
        });


        /*
            Close sockets listening
        */
        socket.addEventListener('close', (event) => {
            console.log('WebSocket connection closed:', event);
        });
        
        document.addEventListener('keydown', function(event) {
            const key = event.key;
        
            socket.send(JSON.stringify({
                type: 'keypress',
                key: key,
            }));
        });
    }
}());



/*
    Backend socket message handler
*/

function handleMessage(data) {
    switch (data.type) {
        case 'users_list':
            updateUsersList(data.users_list, data.max_player);
            break;
        case 'name':
            updatePlayerName(data.name);
            break;
        case 'player_info':
            setPLayerObject(player, data);
            break;
        case 'game_start':
            gameStart()
            break;
        case 'game_update':
            drawGame(data.data);
            break;
        default:
            console.warn('Unknown message type:', data.type);
            console.warn(data);
    }
}


/*
    You can call your function here
    The function draw game will be call each time when a event with new game data is received from the server
*/

function drawGame(data) {
    dessinerPong(data); //function for 
}
