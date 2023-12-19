function getUserInfo() {
    const url = backendUrl + '/authentification/user_info/';

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
		credentials: "include",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Request failed');
        }
        return response.json();
    })
    .then(data => {
        const username = data.username;

        const userInfoElement = document.getElementById('user_info');
        if (userInfoElement) {
            userInfoElement.innerText = `${username}`;
        }
    })
    .catch(error => {
        console.error('Error while reading data in response.', error);
    });
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

getUserInfo();

const logoutBtn = document.getElementById("logout_btn");

logoutBtn.addEventListener("click", function() {
	logout();
})