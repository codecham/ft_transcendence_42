from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Room
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

