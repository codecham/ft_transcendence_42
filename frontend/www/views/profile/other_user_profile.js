const profileElem = document.getElementById('profile_id_elem');
const errorElem = document.getElementById('error_id_elem');


function getUserName() {
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
        var username = paramsObject['username'];
	
        if (username !== "undefined") {
            return(username);
        } else {
            showError('username value not found on the url');
            return(undefined);
        }
    } else {
		showError('username value not found on the url');
        return(undefined)
    }
}

async function fetchData(username) {
    const url = backendUrl + `/user_profile/get_other_user_profile/${username}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
			if (response.status == 404) {
				profileElem.style.display = 'none';
				errorElem.style.display = 'block';
			}
			console.log('1');
            throw new Error(`Request failed: ${response.status}`);
        }

        const jsonResponse = await response.json();
        return jsonResponse;

    } catch (error) {
		console.log('2');
        console.error('Request failed:', error);
    }
}

async function addData(username) {
    const jsonResponse = await fetchData(username);
    const unsername_field = document.getElementById("username_field");
    unsername_field.innerText = jsonResponse.username;
}

const username = getUserName() 
addData(username);




const profileImageUrl = backendUrl + `/user_profile/get_other_profile_image/${username}`;
try {
    fetch(profileImageUrl)
        .then(response => {
            if (!response.ok) {
				profileElem.style.display = 'none';
				errorElem.style.display = 'block';
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.blob();
        })
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            const profileImageElement = document.getElementById('avatar');
            profileImageElement.src = imageUrl;
        })
        .catch(error => {
			profileElem.style.display = 'none';
			errorElem.style.display = 'block';
            console.error("Error while getting profile image: ", error);
        });
} catch (error) {
    console.error("Erreur lors de la requête fetch: ", error);
}



	async function get_match_history() {
        const url = backendUrl + `/game/get_other_game_history/${username}`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                credentials: 'include'
            });
    
            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }
    
            const jsonResponse = await response.json();
            return jsonResponse;
    
        } catch (error) {
            console.error('Request failed:', error);
        }
    }
    
	async function print_match_history() {
        const jsonResponse = await get_match_history();
        console.log("match-history received:");
        console.log(JSON.stringify(jsonResponse, null, 4))
    
        var tbody = document.getElementById('gameHistoryTableBody');
    
        jsonResponse.game_history.forEach(function (game) {
            var row = document.createElement('tr');
    
            var dateCell = document.createElement('td');
            dateCell.textContent = game.created_at;
            dateCell.className = 'dateCell';
            row.appendChild(dateCell);
    
            var player1Cell = document.createElement('td');
            player1Cell.textContent = game.player1_username;
            player1Cell.className = 'player1Cell';
            row.appendChild(player1Cell);
    
            var player2Cell = document.createElement('td');
            player2Cell.className = 'player2Cell';
            player2Cell.textContent = game.player2_username;
            row.appendChild(player2Cell);
    
            var resultCell = document.createElement('td');
            resultCell.textContent = game.is_winner ? 'WIN' : 'LOSE';
            resultCell.className = game.is_winner ? 'win-cell' : 'lose-cell';
            console.log('adding class name....');
            row.appendChild(resultCell);
    
            tbody.appendChild(row);
        });
    }
    
