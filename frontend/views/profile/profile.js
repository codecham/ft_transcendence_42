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