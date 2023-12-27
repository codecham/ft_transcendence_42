from .models import Room, Player, Game

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


class Match:
	def __init__(self, winner, loser, round):
		self.winner = winner
		self.loser = loser
		self.round = round


class Tournament:
	def __init__(self, room_id):
		self.room_id = room_id
		self.round = 1
		self.players_in_round = []
		self.players_eleminated = []
		self.players_next_round = []
		self.matches = []
		self.is_started = False
		self.status = 'ongoing'
		self.winner = None
        
	def add_player(self, player):
		self.players_in_round.append(player)

	
	def get_players_for_next_match(self):
		players_next = []
		players_next.append(self.players_in_round[0])
		players_next.append(self.players_in_round[1])

	
	def add_match_finished(self, winner, loser):
		match = Match(winner, loser, self.round)
		self.matches.append(match)
		self.players_next_round.append(winner)
		self.players_eleminated.append(loser)
		self.players_in_round = self.players_in_round[2:]
		if len(self.players_in_round) < 2:
			if len(self.players_in_round) == 1:
				self.players_next_round.append(self.players_in_round[0])
				self.players_in_round.clear()
			self.players_in_round = self.players_next_round.copy()
			self.players_next_round.clear()
			self.round += 1
			if self.players_in_round == 1:
				self.status = 'finished'
				self.winner = self.players_in_round[0]


	

	def log_tournament(self):
		print(f"{MAGENTA}round = {self.round}")
		print(f"{MAGENTA}player_in_round = {self.players_in_round}")
		print(f"{MAGENTA}player_eleminated = {self.players_eleminated}")
		print(f"{MAGENTA}player_next_round = {self.players_next_round} {RESET}")
	

