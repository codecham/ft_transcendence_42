import { recievedata } from "./pong.js";
import { startGame } from "./pong.js";
import { stopGame } from "./pong.js";


let player = {};
let socket;

//Lobby div
let lobby_div = document.getElementById("lobby-div")
const start_btn = document.getElementById("start_btn_id")
const username_field_elemt = document.getElementById("username-btn")


//Game Div
let pongCanvas = document.getElementById("pongDiv")


//End div
let endGamediv = document.getElementById('endGameDiv')

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

function process_cli(cliInput, errorMessage){
    var command = cliInput.value.trim();

    if (isValidCommand(command)) {
        // Do something with the valid command (you can replace this with your logic)
        console.log("Command entered: " + command);
        errorMessage.textContent = ""; // Clear error message
    } else {
        // Display an error message for invalid command
        errorMessage.textContent = "Invalid command. Please try again.";
    };
    cliInput.value = "";
    var parse = command.split('=');
    console.log(parse);
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "command",
            command: parse[0],
            value: parse[1],
        }));
    } else {
        console.error('WebSocket connection is not open.');
    }
}

function isValidCommand(command) {
    var pattern = /^[a-zA-Z_]+\s*=\s*\d+$/;
    return pattern.test(command);
}

document.addEventListener('DOMContentLoaded', function() {
	const room_id = getRoomId();
    var cliInput = document.getElementById('cli-input');
    var errorMessage = document.getElementById('error-message');

    cliInput.addEventListener('keydown', function (event){
        if (event.key == 'Enter' && !event.shiftKey){
            event.preventDefault();
            process_cli(cliInput, errorMessage);
        }
    });

    if (room_id !== undefined) {
        const socketUrl = `wss://localhost:8001/ws/game/${room_id}/`
        // const socketUrl = socketUrl + `/game/${room_id}/`

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
            const arrowKeys = ['ArrowUp', 'ArrowDown'];

            if (arrowKeys.includes(event.key)) {
                event.preventDefault();
            }
        
            socket.send(JSON.stringify({
                type: 'keypress',
                key: key,
            }));
        });
    }
}());


function change_screen(data) {
    const screenType = data.screen_type

    if (screenType == 'game') {
        lobby_div.style.display = 'none';
        endGamediv.display = 'none';
        pongCanvas.display = 'block';
    }
    if (screenType == 'end_game') {
        stopGame();
        lobby_div.style.display = 'none';
        endGamediv.style.display = 'block';
        pongCanvas.style.display = 'none';
    }
}

function islocal() {
    let controlDiv = document.getElementById('controls');
    let title = document.createElement('h5');
    let control_1 = document.createElement('div');
    let control_2 = document.createElement('div');

    title.textContent = 'Controls:';
    control_1.textContent = 'Player 1: UP: W | DOWN: S';
    control_2.innerHTML = 'Player 2: UP: &uarr; | DOWN: &darr;';
    control_1.style.color = 'white';
    control_2.style.color = 'white';
    controlDiv.appendChild(title);
    controlDiv.appendChild(control_1);
    controlDiv.appendChild(control_2);
    controlDiv.appendChild(document.createElement('br'))


    let titlePage = document.getElementById('title_page');
    titlePage.innerText = "";
    titlePage.innerText = "Local Game";

    const playerListElem = document.getElementById("player-list-settings");
    playerListElem.style.display = 'none';
}


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
        case 'change_screen':
            change_screen(data.data)
            break;
        case 'stat_game':
            startGameEvent()
            break;
        case 'game_update':
            drawGame(data.data)
            break;
        case 'game_end':
            endGame(data.data)
            break;
        case 'is_local':
            islocal()
            break;
        default:
            console.warn('Unknown message type:', data.type);
            console.warn(data);
    }
}
/*---------------------------------------------------*/




function startGameEvent() {
    startGame();
}



function drawGame(data) {
    recievedata(data);
}

/*
    You can call your function here
    The function draw game will be call each time when a event with new game data is received from the server
*/

function endGame(data) {
    let winnerNameElem = document.getElementById('winner_name');
    let loserNameElem = document.getElementById('loser_name');
    const winner = data.winner_name;
    const loser = data.loser_name;
    stopGame();

    winnerNameElem.innerText = winner;
    loserNameElem.innerText = loser;
}
