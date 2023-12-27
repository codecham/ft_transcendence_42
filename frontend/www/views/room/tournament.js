import { recievedata } from "./pong.js";
import { startGame } from "./pong.js";


let player = {};
let socket;

//Lobby div
const lobby_div = document.getElementById("lobby-div")
const start_btn = document.getElementById("start_btn_id")
const username_field_elemt = document.getElementById("username-btn")


//Game Div
const pongCanvas = document.getElementById("pongDiv")


//End div
const endGamediv = document.getElementById('endGameDiv')


//Lobby div Function
/*---------------------------------------------------*/
start_btn.addEventListener('click', sendStartGame)

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
    // startGame();
}


//Create player object
function setPLayerObject(player, data) {
    player.name = data.name;
    player.slot = data.slot;
    player.is_master = data.is_master;
    username_field_elemt.innerText = ''
    username_field_elemt.innerText = player.name
    if (player.is_master != true) {
        start_btn.style.display = 'none';
    }
}


function setPlayerList(data) {
    const playerListElem = document.getElementById("player-list-settings");
    const players_list = data.players;

    playerListElem.innerHTML = "";

    for (let i = 1; i <= players_list.length; i++) {
        const player = players_list[i - 1];

        const li = document.createElement("li");

        const playerText = `Player ${i}: `;

        const span = document.createElement("span");

        if (player.name !== "none") {
            span.style.fontSize = "17px";
            span.style.color = "#188034";
            span.textContent = player.name;
        } else {
            span.style.fontSize = "14px";
            span.style.color = "gray";
            span.textContent = "waiting player...";
        }

        li.appendChild(document.createTextNode(playerText));
        li.appendChild(span);
        
        playerListElem.appendChild(li);
    }
}

function setNumberOfPlayer(data) {
    const nbPlayerElem = document.getElementById("nb_player_button");
    nbPlayerElem.innerText = "";
    nbPlayerElem.innerText = data.nb_players;
}



/*---------------------------------------------------*/








//Socket Function
/*---------------------------------------------------*/
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
        case 'player_info':
            setPLayerObject(player, data.data);
            break;
        case 'player_list_slot':
            setPlayerList(data.data)
            break;
        case 'nb_players':
            setNumberOfPlayer(data.data)
            break;
        default:
            console.warn('Unknown message type:', data.type);
            console.warn(data);
    }
}
/*---------------------------------------------------*/






/*
    You can call your function here
    The function draw game will be call each time when a event with new game data is received from the server
*/

function endGame(data) {

}

function drawGame(data) {
    game_message_elem.innerText = '';
    recievedata(data);
}
