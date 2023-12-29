from .models import Room, Player, Game
import copy

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
	def __init__(self, player_list):
		self.round = 1
		self.current_round_players = copy.deepcopy(player_list)
		self.next_round_players = []
		self.elimined_players = []
		self.matches = []
		self.finished = False
		self.winner = None

	def get_players_for_next_match(self):
		player1 = self.current_round_players[0]
		player2 = self.current_round_players[1]

		return player1, player2
	
	def save_and_set_next_mach(self, winner_name, loser_name):
		match = Match(winner_name, loser_name, self.round)
		
		self.matches.append(match)
		
		if winner_name == self.current_round_players[0].name:
			self.next_round_players.append(self.current_round_players[0])
			self.elimined_players.append(self.current_round_players[1])
		else:
			self.next_round_players.append(self.current_round_players[1])
			self.elimined_players.append(self.current_round_players[0])
		
		self.set_next_match()
	
	def set_next_match(self):
		self.current_round_players.pop(0)
		self.current_round_players.pop(0)
		if len(self.current_round_players) <= 1:
			if len(self.current_round_players) == 1:
				player = self.current_round_players.pop(0)
				self.next_round_players.append(player)
			self.round += 1
			if len(self.next_round_players) == 1 and len(self.current_round_players) == 0:
				self.finished = True
				self.winner = self.next_round_players[0].name
			else:
				self.current_round_players = copy.deepcopy(self.next_round_players)
				self.next_round_players.clear()
		
		
	def is_finished(self):
		return self.is_finished

	def get_matches_list(self):
		matches_list = []

		for match in self.matches:
			match_dict = {
				"winner": match.winner,
				"loser": match.loser,
				"round": match.round
			}
			matches_list.append(match_dict)

		return matches_list