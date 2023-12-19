from django.db import models
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLACK = "\033[30m"
WHITE = "\033[97m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

# Create your models here.


class Game(models.Model):
	game_id = models.AutoField(primary_key=True)
	player1_id = models.IntegerField(default=0)
	player2_id = models.IntegerField(default=0)
	ball_pos_x = models.FloatField(default=0)
	ball_pos_y = models.FloatField(default=0)
	p1_pos = models.FloatField(default=0)
	p2_pos = models.FloatField(default=0)
	score_p1 = models.PositiveIntegerField(default=0)
	score_p2 = models.PositiveBigIntegerField(default=0)
	map = models.IntegerField(default=0)
	status = models.CharField(max_length=20, choices=[
		('pending', 'Pending'),
		('ongoing', 'Ongoing'),
		('finished', 'Finished'),
		('pause', 'Pause')
	])

class Player(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	name = models.CharField(max_length=255, blank=True)
	room_id = models.PositiveBigIntegerField(default=0)
	slot = models.PositiveBigIntegerField(default=0)
	is_connected = models.BooleanField(default=True)
    

class Room(models.Model):
	room_id = models.AutoField(primary_key=True)
	creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	master_user_id = models.PositiveBigIntegerField(default=0)
	max_player = models.PositiveIntegerField()
	is_tournament = models.BooleanField(default=False)
	players_connected = models.ManyToManyField(Player, related_name='connected_rooms')
	player_slots = models.JSONField(default=dict)
	game_started = models.BooleanField(default=False)
	current_game_id = models.IntegerField(blank=True, default=0)

	def save(self, *args, **kwargs):
		if not self.pk:
			self.initialize_player_slot()
		super().save(*args, **kwargs)

	def initialize_player_slot(self):
		self.player_slots = {str(i): '' for i in range(1, self.max_player + 1)}
	
	def add_user_to_slot(self, user_id):
		if user_id in self.player_slots.values():
			position = next((pos for pos, value in self.player_slots.items() if value == user_id), None)
			return position
		for position, value in self.player_slots.items():
			if not value:
				self.player_slots[position] = user_id
				self.save()
				break
		return position
	
	def remove_user_from_slot(self, user_id):
		for position, value in self.player_slots.items():
			if value == user_id:
				self.player_slots[position] = ''
				self.save()
				break

	def get_player_slots(self):
		return self.player_slots

	def print_value_db(self):
		connected_users = self.players_connected.all()
		print(f"{MAGENTA}Log of room [{self.room_id}] in model {RESET}")
		print(f"{MAGENTA}Connected_user [{[user.user for user in connected_users]}]{RESET}")
		print(f"{MAGENTA}Player Slot [{self.player_slots}]{RESET}")


	def add_user_to_players_connected(self, player):
		self.players_connected.add(player)
		self.save()

	def remove_user_from_players_connected(self, user, slot):
		try:
			player = Player.objects.get(user=user, room_id=self.room_id, slot=slot)
			self.players_connected.remove(player)
		except Player.DoesNotExist:
			print("Error while disconnected user. Not in the room")
		self.save()


	def get_connected_players(self):
		connected_players = self.players_connected.all()
		return list(connected_players.values('name', 'slot'))
	
	def get_max_player(self):
		return self.max_player

	def has_master_player(self):
		if self.master_user_id == 0:
			return False
		else:
			return True
	
	def set_user_master(self, user_id):
		self.master_user_id = user_id
		self.save()

	def remove_master(self, user_id):
		if self.master_user_id == user_id:
			self.master_user_id = 0
			self.save()

	def get_player_by_user_id(self, user_id):
		try:
			return self.players_connected.get(user_id=user_id)
		except Player.DoesNotExist:
			return None

	def get_number_of_players_connected(self):
		return self.players_connected.count()

	def set_game_start(self, value):
		self.game_started = value
		self.save()
	
	def get_game_start(self):
		return self.game_started
	
	def get_is_tournament(self):
		return self.is_tournament
	
	def player_is_in_slot(self, user_id):
		return user_id in self.player_slots.values()
	
	def set_player_connexion(self, user_id, value):
		try:
			player = self.players_connected.get(user_id=user_id)
			player.is_connected = value
			player.save()
		except Player.DoesNotExist:
			print("Player not found in players_connected.")
		
	def get_player_is_connected(self, user_id):
		try:
			player = self.players_connected.get(user_id=user_id)
			return player.is_connected
		except Player.DoesNotExist:
			print("Player not found in players_connected.")
			return None
	
	def get_player_by_slot(self, slot):
		try:
			return self.players_connected.get(slot=slot)
		except Player.DoesNotExist:
			return None
		
	def set_current_game(self, game_id):
		self.current_game_id = game_id
		self.save()


		

