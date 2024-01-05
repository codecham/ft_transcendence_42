from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from .models import Room, Game
from authentification.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_room_view(request):
	new_room = Room.objects.create(creator=request.user, max_player=2, is_tournament=False)
	new_room_id = new_room.room_id

	return (JsonResponse({"room_id": new_room_id}))

@login_required
def create_tournement_view(request, nb_player):
	if nb_player < 3 or nb_player > 8:
		return (JsonResponse({"error":"number of players must be between 3 and 8"}, status=400))
	new_room = Room.objects.create(creator=request.user, max_player=nb_player, is_tournament=True)
	new_room_id = new_room.room_id

	return (JsonResponse({"room_id": new_room_id}))

@login_required
def create_local_game_view(request):
	new_room = Room.objects.create(creator=request.user, max_player=1, is_local=True)
	new_room_id = new_room.room_id
	return (JsonResponse({"room_id": new_room_id}))


@login_required
def get_match_history(request):
	if request.method != "GET":
		return JsonResponse({'error': 'Method not allowed.'}, status=405)
	
	user = request.user
	games = Game.objects.filter(player1_id=user.id) | Game.objects.filter(player2_id=user.id)

	game_history = []

	for game in games:
		player1_username = get_object_or_404(UserProfile, id=game.player1_id).username
		player2_username = get_object_or_404(UserProfile, id=game.player2_id).username
		winner_username = get_object_or_404(UserProfile, id=game.winner_id).username
		loser_username = get_object_or_404(UserProfile, id=game.loser_id).username

		is_winner = game.winner_id == int(user.id)

		game_data = {
			'player1_username': player1_username,
			'player2_username': player2_username,
			'winner_username': winner_username,
			'loser_username': loser_username,
			'created_at': game.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			'is_winner': is_winner,
		}

		game_history.append(game_data)

	return JsonResponse({'game_history': game_history})



@login_required
def get_other_game_history(request, username):
	user = get_object_or_404(UserProfile, username=username)

	if not user:
		return JsonResponse({'error': 'User not found.'}, status=404)

	games = Game.objects.filter(player1_id=user.id) | Game.objects.filter(player2_id=user.id)

	game_history = []

	for game in games:
		player1_username = get_object_or_404(UserProfile, id=game.player1_id).username
		player2_username = get_object_or_404(UserProfile, id=game.player2_id).username
		winner_username = get_object_or_404(UserProfile, id=game.winner_id).username
		loser_username = get_object_or_404(UserProfile, id=game.loser_id).username

		is_winner = game.winner_id == int(user.id)

		game_data = {
			'player1_username': player1_username,
			'player2_username': player2_username,
			'winner_username': winner_username,
			'loser_username': loser_username,
			'created_at': game.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			'is_winner': is_winner,
		}

		game_history.append(game_data)

	return JsonResponse({'game_history': game_history})
