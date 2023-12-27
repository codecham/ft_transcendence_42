from .models import Room
# from .player import Player

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


class RoomPong:
	def __init__(self, room):
		self.room_id = room.room_id
		self.max_players = room.max_player
		self.is_tournament = room.is_tournament
		self.is_local = room.is_local
		self.players_slot = {slot: None for slot in range(1, self.max_players + 1)}
		self.master = None
		self.status = 'lobby'
		self.connected_players = []
		self.current_game = None

	#Add a player to the first slot
	def add_player_to_first_available_slot(self, player):
		for slot, player_in_slot in self.players_slot.items():
			if player_in_slot is None:
				self.players_slot[slot] = player
				player.slot = slot
				if slot == 1:
					player.isMaster = True
					self.master = player
				print(f"{GREEN}Room [{self.room_id}]: add player {player.name} to slot {slot}{RESET}")
				return slot
		print(f"{RED}Room [{self.room_id}] is full. Player can't be added")
		return None
	
	#Remove a user
	def remove_player_slot(self, player):
		for slot, player_in_slot in self.players_slot.items():
			if player_in_slot == player:
				self.players_slot[slot] = None
				if slot == 1:
					player.isMaster = False
					self.master = None
				return True 
		print(f"{RED}Room [{self.room_id}]: player is not in the room.{RESET}")
		return False
	
	def get_slot(self):
		return self.players_slot
	
	def add_player_connected(self, player):
		self.connected_players.append(player)

	def remove_player_connected(self, player):
		if player in self.connected_players:
			self.connected_players.remove(player)

	def get_connected_players(self):
		return self.connected_players
	
	def is_player_connected(self, player):
		for connected_player in self.connected_players:
			if connected_player.user_id == player.user_id:
				return True
		return False
	
	def get_player_slot(self, player_id):
		for slot, player_in_slot in self.players_slot.items():
			if player_in_slot is not None and player_in_slot.user_id == player_id:
				return slot

		print(f"{RED}Player with user_id {player_id} is not in the room.{RESET}")
		return None
	

	def get_player_by_slot(self, slot):
		return self.players_slot.get(slot, None)



	def room_is_full(self):
		return len(self.connected_players) >= self.max_players
	



	#log function:
	def print_slots(self):
		print(f"{MAGENTA}Slots:{RESET}")
		for slot, player_in_slot in self.players_slot.items():
			if player_in_slot is not None:
				print(f"{MAGENTA}	Slot [{slot}]:{BLUE} [{player_in_slot.name}]{RESET}")
			else:
				print(f"{MAGENTA}	Slot [{slot}]:{BLUE} [empty]{RESET}")
	
	def print_connected_player(self):
		print(f"{MAGENTA}Players connected:{RESET}")
		for player in self.connected_players:
			print(f"{MAGENTA}-	{BLUE}[{player.name}]{RESET}")

	
	def log_room(self):
		print(f"{MAGENTA}Log for room [{self.room_id}]:{RESET}")
		print(f"{MAGENTA}	Max_player:{BLUE} [{self.max_players}]{RESET}")
		print(f"{MAGENTA}	Is_tounament:{BLUE} [{self.is_tournament}]{RESET}")
		print(f"{MAGENTA}	Is_local:{BLUE} [{self.is_local}]{RESET}")
		print(f"{MAGENTA}	status:{BLUE} [{self.status}]{RESET}")
		if self.master != None:
			print(f"{MAGENTA}	Master:{BLUE} [{self.master.name}]{RESET}")
		else:
			print(f"{MAGENTA}	Master:{BLUE} [None]{RESET}")
		self.print_connected_player()
		self.print_slots()

	def set_current_game(self, game):
		self.current_game = game



