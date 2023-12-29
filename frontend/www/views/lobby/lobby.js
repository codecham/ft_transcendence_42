document.getElementById('single_game_btn').addEventListener('click', createRoom);
document.getElementById('tournament_btn').addEventListener('click', createTournament);
document.getElementById('Local_game_btn').addEventListener('click', createLocalGame);


function createLocalGame() {
	const url = backendUrl + "/game/create_local/";

	fetch(url)
		.then(response => {
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}
			return response.json();
		})
		.then(data => {
			const roomId = data.room_id;
			console.log(`Room created with success: Room_id: ${roomId}`);
			window.location.hash = `room?room_id=${roomId}`;
		})
		.catch(error => {
			console.error('Error while room creation', error);
		});

}


function createRoom() {
	const url = backendUrl + "/game/create_room/";

	fetch(url)
		.then(response => {
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}
			return response.json();
		})
		.then(data => {
			const roomId = data.room_id;
			console.log(`Room created with success: Room_id: ${roomId}`);
			window.location.hash = `room?room_id=${roomId}`;
		})
		.catch(error => {
			console.error('Error while room creation', error);
		});
}

function createTournament() {
	let url = backendUrl + "/game/create_tournement/";
	let selectNumber = 3;

	document.getElementById("container-button_id").style.display = 'none';
	document.getElementById("container_tournament_id").style.display = 'block';
    
	const numbers = document.querySelectorAll('.number');
	numbers.forEach(number => {
		number.addEventListener('click', function() {
			numbers.forEach(num => num.classList.remove('selected'));
			number.classList.add('selected');
			selectNumber = parseInt(number.textContent);
		});
	});

	const backButton = document.getElementById('backButton');
	backButton.addEventListener('click', function() {
		document.getElementById("container-button_id").style.display = 'block';
		document.getElementById("container_tournament_id").style.display = 'none';
	});

	const createButton = document.getElementById('createButton');
	createButton.addEventListener('click', function() {
		console.log('Create button clicked');
		url += selectNumber;
		console.log("url: " + selectNumber);
		fetch(url)
		.then(response => {
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}
			return response.json();
		})
		.then(data => {
			const roomId = data.room_id;
			console.log(`Room created with success: Room_id: ${roomId}`);
			window.location.hash = `tournament?room_id=${roomId}`;
		})
		.catch(error => {
			console.error('Error while room creation', error);
		});

	});	
}
