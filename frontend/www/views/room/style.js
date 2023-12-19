const playerButton = document.getElementById("player-button");

playerButton.addEventListener('click', showPlayer)

function showPlayer() {
	let playerList = document.getElementById("player-list");

	if (playerList.style.display === 'block') {
		playerList.style.display = 'none';
	} else
		playerList.style.display = 'block'
}