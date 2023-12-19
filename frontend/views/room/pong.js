const terrainXMin = -6;
const terrainXMax = 6;
const terrainYMin = -4;
const terrainYMax = 4;
const raquetteTaille = 1.5;
const balleTaille = 0.2;
const screen_x = 1200;
const screen_y = 800;
const x_scale = 12
const y_scale = 8
const score_div = document.getElementById("score")


export function convertCoordX(value)
{
	const scale = screen_x / x_scale;
	const middle = screen_x / 2;

	if (value == 0)
		return (middle)
	else if (value < 0)
		return(middle + (scale * value));
	else
		return(middle - (scale * (value * -1)))
}

export function convertCoorY(value)
{
	const scale = screen_y / y_scale;
	const middle = screen_y / 2;

	if (value == 0)
		return (middle)
	else if (value < 0)
		return(middle + (scale * value));
	else
		return(middle - (scale * (value * -1)))
}

export function convertValueX(value)
{
	const scale = screen_x / x_scale;
	return value * scale
}

export function convertValueY(value)
{
	const scale = screen_y / y_scale;
	return value * scale
}



export function dessinerPong(data) {
	var canvas = document.getElementById("pongCanvas");
	var context = canvas.getContext("2d");
  
	context.clearRect(0, 0, canvas.width, canvas.height);
  
	// Définir les propriétés du jeu
  
	// Convertir les coordonnées du JSON aux coordonnées du canvas
	var p1_y = data.p1_posY
	var p2_y = data.p2_posY
	var ball_x = data.ball_posX
	var ball_y = data.ball_posY
	var p1_score = data.p1_score
	var p2_score = data.p2_score
	var status = data.status
	var winner = data.winner
	var loser = data.loser

	// var str = JSON.stringify(data);
	// str = JSON.stringify(data, null, 4); // (Optional) beautiful indented output.
	// console.log(str); 
	// console.log(`p1_y = ${p1_y} -- p2_y = ${p2_y} -- ball_x = ${ball_x} -- ball_y = ${ball_y}`);
	console.log(`Convert value p2_y [${p2_y}] --> ${convertCoorY(p2_y)}`)
  
	context.fillStyle = "#FF0000";
	context.fillRect((screen_x / 2) - 1, 0, 3, screen_y)
	context.fillRect(0, (screen_y / 2) - 1, screen_x, 3)
	// Dessiner les raquettes
	context.fillStyle = "#FFFFFF"; // Couleur blanche
	context.fillRect(0, convertCoorY(p1_y) - convertValueY(raquetteTaille) / 2, 10, convertValueY(raquetteTaille));
	context.fillRect(screen_x - 10, convertCoorY(p2_y) - convertValueY(raquetteTaille) / 2, 10, convertValueY(raquetteTaille));
  
	// Dessiner la balle
	// context.fillRect(ball_x - balleTaille / 2, ball_y - balleTaille / 2, balleTaille * canvas.width, balleTaille * canvas.height);
	context.fillRect(convertCoordX(ball_x) - (convertValueY(balleTaille) / 2), convertCoorY(ball_y) - (convertValueY(balleTaille) / 2), convertValueY(balleTaille), convertValueY(balleTaille))
	
	score_div.innerText = '';
	score_div.innerText = `${p1_score} -- ${p2_score}`;
	score_div.style.color = 'gray';
	if (status == 'finished') {
		score_div.innerText = `----- Winner: ${winner} -- Loser: ${loser}`;
	}
  }