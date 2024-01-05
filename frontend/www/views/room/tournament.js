import { recievedata } from "./pong.js";
import { startGame } from "./pong.js";
import { stopGame } from "./pong.js";

let player = {};
let socket;

//Lobby div
let lobby_div = document.getElementById("lobby-div")
const start_btn = document.getElementById("start_btn_id")
const username_field_elemt = document.getElementById("username-btn")
const changeNameBtn = document.getElementById("change_name_btn")
const nameInput = document.getElementById('name-input')
let errorMessageNameElement = document.getElementById('error-message-name')
const cli_log_elem = document.getElementById('cli_log')

//Game Div
let pongCanvas = document.getElementById("pongDiv")


//End div
let endGamediv = document.getElementById('endGameDiv')


//Next Match Div
let nextMatchDiv = document.getElementById('nextMatchDiv')
const startNextMatchButton = document.getElementById('startNextMatchButton')


//End Game Tournament div
let endGameTournamentDiv = document.getElementById('endGameTournamentDiv')
const getNextMacthButton = document.getElementById('getNextMatchButton')

//End Tournament div
let endTournamentDiv = document.getElementById('endTournamendDiv')


//Lobby div Function
/*---------------------------------------------------*/
start_btn.addEventListener('click', sendStartGame);
startNextMatchButton.addEventListener('click', sendStartNextMatch);
getNextMacthButton.addEventListener('click', getNextMatch)
changeNameBtn.addEventListener('click', changeName)



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

function sendStartNextMatch() {
    console.log("Button start next match pressed");
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "action",
            data: "startNextGame",
        }));
    } else {
        console.error('WebSocket connection is not open.');
    }
}

function getNextMatch() {
    console.log("Button start game pressed");
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "action",
            data: "getNextGame",
        }));
    } else {
        console.error('WebSocket connection is not open.');
    }
}


function changeName() {
    var newName = nameInput.value;
    errorMessageNameElement.innerText = ''
    if (newName.length < 4 || newName.length > 25) {
        errorMessageNameElement.innerText = "Name must be between 4 and 25 characters";
        return
    }
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "action",
            data: "changeName",
            name: newName,
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
        getNextMacthButton.style.display = 'none';
    }
    if (player.is_master != true) {
        startNextMatchButton.style.display = 'none';

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


function share_link(room_id) {
    const linkElem = document.getElementById('sharing_link');
    var linkContainer = document.getElementById('share-link-container')
    const url = backendUrl.slice(0, -4);

    linkContainer.style.display = 'block';
    linkElem.innerText = `${url}/#tournament?room_id=${room_id}`;
}



//Socket Function
/*---------------------------------------------------*/
function showError(error) {
    const errorMessageElement = document.getElementById('error-message');

    errorMessageElement.innerHTML = 'Error: ';
    errorMessageElement.innerHTML = error;
}

function showErrorName(data) {
    const name = data.name;

    errorMessageNameElement.innerText = '';
    errorMessageNameElement.innerText = `${name} is already used in this room`;
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

function cli_help() {
    cli_log_elem.innerText= '';
    cli_log_elem.innerText = 'USAGE:\n' +
                             'score_max=[1 - 50]\n' +
                             'timer=[1 - 100]\n' +
                             'player_speed=[1 - 3]\n' +
                             'ball_speed_x=[0.1 - 0.3]';
}


function process_cli(cliInput, errorMessage){
    var command = cliInput.value.trim();

    if (command == 'help') {
        cli_help();
        return ;
    }
    if (isValidCommand(command)) {
        console.log("Command entered: " + command);
        cli_log_elem.textContent = "";
    } else {
        cli_log_elem.textContent = "Invalid command. Please try again.";
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
    var pattern = /^[a-zA-Z_]+\s*=\s*-?\d+(\.\d+)?$/;
    return pattern.test(command) && !/\s/.test(command);
}


document.addEventListener('DOMContentLoaded', function() {
	const room_id = getRoomId();
    var cliInput = document.getElementById('cli-input');
    var errorMessage = document.getElementById('error-message');

    if (room_id !== undefined) {
        const socketUrl = `${g_socketsUrl}${room_id}/`;
        console.log("url socket: ", socketUrl);
        socket = new WebSocket(socketUrl);

        /*
            Open socket listening
        */
        socket.addEventListener('open', (event) => {
            console.log('WebSocket connection established:', event);
            share_link(room_id);
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

        cliInput.addEventListener('keydown', function (event){
            if (event.key == 'Enter' && !event.shiftKey){
                event.preventDefault();
                process_cli(cliInput, errorMessage);
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
        endGamediv.style.display = 'none';
        pongCanvas.style.display = 'block';
        nextMatchDiv.style.display = 'none';
        endGameTournamentDiv.style.display = 'none';
        endTournamentDiv.style.display = 'none';
    }
    else if (screenType == 'end_game') {
        stopGame();
        lobby_div.style.display = 'none';
        endGamediv.style.display = 'block';
        pongCanvas.style.display = 'none';
        nextMatchDiv.style.display = 'none';
        endGameTournamentDiv.style.display = 'none'
        endTournamentDiv.style.display = 'none';
    }
    else if (screenType == 'next_match') {
        lobby_div.style.display = 'none';
        endGamediv.style.display = 'none';
        pongCanvas.style.display = 'none';
        nextMatchDiv.style.display = 'block';
        endGameTournamentDiv.style.display = 'none';
        endTournamentDiv.style.display = 'none';
    }
    else if (screenType == 'end_game_tournament') {
        stopGame();
        lobby_div.style.display = 'none';
        endGamediv.style.display = 'none';
        pongCanvas.style.display = 'none';
        nextMatchDiv.style.display = 'none';
        endGameTournamentDiv.style.display = 'block';
        endTournamentDiv.style.display = 'none';
    }
    else if (screenType == 'end_tournament') {
        stopGame();
        lobby_div.style.display = 'none';
        endGamediv.style.display = 'none';
        pongCanvas.style.display = 'none';
        nextMatchDiv.style.display = 'none';
        endGameTournamentDiv.style.display = 'none';
        endTournamentDiv.style.display = 'block';

    }
}


function cli_log(message) {
    cli_log_elem.innerText = '';
    cli_log_elem.innerText = message;
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
        case 'player_next_match':
            nextMatchEvent(data.data)
            break;
        case 'game_end_tournament':
            gameEndTournament(data.data)
            break
        case 'tounrnament_end':
            endTournament(data.data)
            break;
        case 'name_already_use':
            showErrorName(data.data)
            break
        case 'cli_log':
            cli_log(data.data.message)
            break;
        default:
            console.warn('Unknown message type:', data.type);
            console.warn(data);
    }
}
/*---------------------------------------------------*/



function endTournament(data) {
    const winner = data.winner;
    const matchList = data.matches_list;
    let winnerElem = document.getElementById('winner_name_end_tournament');
    let matchListElem = document.getElementById('matchList');

    winnerElem.innerText = '';
    winnerElem.innerText = winner;
    for (let i = 1; i <= matchList.length; i++) {
        let match = matchList[i - 1];
        //create div
        let row = document.createElement('div');
        row.classList.add('row');

        //create match elem
        let line_1 = document.createElement('div');
        line_1.classList.add('col-sm');
        line_1.textContent = `Match ${i}`;
        row.appendChild(line_1);

        //create VS elem
        let line_2 = document.createElement('div');
        line_2.classList.add('col-sm');
        let span_p1 = document.createElement('span');
        let span_p2 = document.createElement('span');
        let vs_span = document.createElement('span');
        span_p1.classList.add("p_tournament_list");
        span_p2.classList.add("p_tournament_list");
        span_p1.textContent = `${match.winner}`;
        span_p2.textContent = `${match.loser}`;
        vs_span.textContent = ` VS `;
        line_2.appendChild(span_p1);
        line_2.appendChild(vs_span);
        line_2.appendChild(span_p2);
        row.appendChild(line_2);

        //create Winner elem
        let line_3 = document.createElement('div');
        line_3.classList.add('col-sm');
        line_3.textContent = 'Qualified: ';
        let span_winner = document.createElement('span');
        span_winner.classList.add('p_tournament_list_qualified');
        span_winner.textContent = `${match.winner}`;
        line_3.appendChild(span_winner);
        row.appendChild(line_3);
        
        matchListElem.appendChild(row);
    }
}

function gameEndTournament(data) {

    const winner_name = data.winner_name;
    const loser_name = data.loser_name;
    let winner_elem = document.getElementById('winner_name_tournament');
    let loser_elem = document.getElementById('loser_name_tournament');

    winner_elem.innerText = '';
    loser_elem.innerText = '';
    winner_elem.innerText = winner_name;
    loser_elem.innerText = loser_name;
}


function nextMatchEvent(data) {
    const p1_name = data.player_1;
    const p2_name = data.player_2;
    let p1_elem = document.getElementById('player1Name');
    let p2_elem = document.getElementById('player2Name');

    p1_elem.innerText = '';
    p2_elem.innerText = '';
    p1_elem.innerText = p1_name;
    p2_elem.innerText = p2_name;
}


function startGameEvent() {
    startGame();
}



function drawGame(data) {
    recievedata(data);
}




function endGame(data) {
    let winnerNameElem = document.getElementById('winner_name');
    let loserNameElem = document.getElementById('loser_name');
    const winner = data.winner_name;
    const loser = data.loser_name;
    stopGame();

    winnerNameElem.innerText = winner;
    loserNameElem.innerText = loser;
}
