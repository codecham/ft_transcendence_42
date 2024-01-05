'use strict'

async function fetchData() {
    const url = backendUrl + "/user_profile/get_profile/";
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

async function addData() {
    const jsonResponse = await fetchData();
    const unsername_field = document.getElementById("username_field");
    unsername_field.innerText = jsonResponse.username;
}

function logout() {
	const url = backendUrl + '/authentification/logout/';

	fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': 'http://localhost:8080',
			'Access-Control-Allow-Credentials': 'true'
        },
		credentials: 'include',
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error during deconnexion', data.error);
        } else {
            console.log('Logout successfull.');
            window.location.hash = `sign-in`;
        }
    })
    .catch(error => {
        console.error('Error while reading data in response.', error);
    });
}

addData();

const logoutBtn = document.getElementById("logout-btn");
logoutBtn.addEventListener("click", function() {
	logout();
})

const profileImageUrl = backendUrl+"/user_profile/get_profile_image/";

// Utilisez fetch pour récupérer l'image
fetch(profileImageUrl)
    .then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.blob();
    })
    .then(blob => {
    // Convertissez le blob en URL d'objet
    const imageUrl = URL.createObjectURL(blob);

    // Utilisez imageUrl comme source pour votre image HTML
    const profileImageElement = document.getElementById('avatar');
    profileImageElement.src = imageUrl;
    })
    .catch(error => {
    console.error("Erreur lors de la récupération de l'image de profil:", error);
    });

    // -----------------------------

    async function get_match_history() {
        const url = backendUrl + '/game/get_match_history/';
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
    
    print_match_history();