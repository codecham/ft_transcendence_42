from .models import Room, Player, Game
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

UP = 'ArrowUp'
DOWN = 'ArrowDown'
PADDLE_SIZE = 1.5
PADDLE_WIDTH = 0.2
MAP_SIZE_X = 12
MAP_SIZE_Y = 8
BALL_SPEED_X = 0.3
BALL_SPEED_Y = 0.1
BALL_SIZE = 0.2
PLAYER_SPEED = 0.2


class Ball:
	MAX_VEL = 0.2

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.x_vel = self.MAX_VEL
		self.y_vel = 0

	def move(self):
		self.x += self.x_vel
		self.y += self.y_vel

class PongGame:
	def __init__(self, room_id, game):
		self.room_id = room_id
		self.game_id = game.game_id
		self.p1 = game.player1_id
		self.p2 = game.player2_id
		self.ball = Ball(0, 0)
		self.p1_y = game.p1_pos
		self.p2_y = game.p2_pos
		self.score_p1 = game.score_p1
		self.score_p2 = game.score_p2
		self.status = game.status
		self.map = game.map
		self.corner_up = (MAP_SIZE_Y / 2) * -1
		self.corner_down = (MAP_SIZE_Y / 2)
		self.run = False
		print(f"{MAGENTA} Room [{self.room_id}] game started with success")

	def get_player(self, player):
		return player.user

	def input_move(self, player_id, key):
		if player_id != self.p1 and player_id != self.p2:
			return
		if player_id == self.p1:
			if key == UP:
				self.p1_y -= PLAYER_SPEED
				if (self.p1_y - (PADDLE_SIZE / 2) < self.corner_up):
					self.p1_y = self.corner_up + (PADDLE_SIZE / 2)
			elif key == DOWN:
				self.p1_y += PLAYER_SPEED
				if (self.p1_y + (PADDLE_SIZE / 2) > self.corner_down):
					self.p1_y = self.corner_down - (PADDLE_SIZE / 2)
		elif player_id == self.p2:
			if key == UP:
				self.p2_y -= PLAYER_SPEED
				if (self.p2_y - (PADDLE_SIZE / 2) < self.corner_up):
					self.p2_y = self.corner_up + (PADDLE_SIZE / 2)
			elif key == DOWN:
				self.p2_y += PLAYER_SPEED
				if (self.p2_y + (PADDLE_SIZE / 2) > self.corner_down):
					self.p2_y = self.corner_down - (PADDLE_SIZE / 2)
	
	def check_run(self):
		if self.status == 'ongoing':
			return True
		else:
			return False
		
	def update_game_state(self):
		self.ball.move()
		self.handle_collision()

		game_state = {
            'ball_posX': self.ball.x,
            'ball_posY': self.ball.y,
            'p1_posY': self.p1_y,
            'p2_posY': self.p2_y,
            'p1_score': self.score_p1,
            'p2_score': self.score_p2,
        }
		return game_state
	

	# def checkColPlayers(self):
	# 	if self.ball_pos_x - (BALL_SIZE / 2) < -6 + (PADDLE_WIDTH / 2):
	# 		if self.ball_pos_y

	def handle_collision(self):
		if self.ball.y > (MAP_SIZE_Y / 2) - (BALL_SIZE / 2):
			self.ball.y_vel *= -1
		elif self.ball.y < (0 - (MAP_SIZE_Y / 2)) + (BALL_SIZE / 2):
			self.ball.y_vel *= -1
		
		if self.ball.x_vel < 0:
			#check left paddle
			if self.ball.x - (BALL_SIZE / 2) <= ((MAP_SIZE_X / 2) * -1) + (PADDLE_WIDTH / 2):
				if self.ball.y - (BALL_SIZE / 2) <= self.p1_y + (PADDLE_SIZE / 2) and self.ball.y + (BALL_SIZE / 2) >= self.p1_y - (PADDLE_SIZE / 2):
					#left paddle hit
					self.ball.x_vel *= -1
					difference_in_y = self.ball.y - self.p1_y
					reduction_factor = (PADDLE_SIZE / 2) / self.ball.MAX_VEL
					self.ball.y_vel = difference_in_y / reduction_factor
				elif self.ball.x <= (MAP_SIZE_X / 2) * -1:
					self.ball.x = 0
		else:
			#check right paddle
			if self.ball.x + (BALL_SIZE / 2) >= (MAP_SIZE_X / 2) - (PADDLE_WIDTH / 2):
				if self.ball.y - (BALL_SIZE / 2) <= self.p2_y + (PADDLE_SIZE / 2) and self.ball.y + (BALL_SIZE / 2) >= self.p2_y - (PADDLE_SIZE / 2):
					#right paddle hit
					self.ball.x_vel *= -1
					difference_in_y = self.ball.y - self.p2_y
					reduction_factor = (PADDLE_SIZE / 2) / self.ball.MAX_VEL
					self.ball.y_vel = difference_in_y / reduction_factor
				elif self.ball.x >= (MAP_SIZE_X / 2):
					self.ball.x = 0



	def get_game_state(self):
		pass

	def log_game(self):
		print(f"{MAGENTA}Game [{self.game_id}]")
		print(f"{MAGENTA}p1 [{self.p1}]")		
		print(f"{MAGENTA}p2 [{self.p2}]")
		print(f"{MAGENTA}ball_pos_x [{self.ball.x}]")
		print(f"{MAGENTA}ball_pos_y [{self.ball.y}]")
		print(f"{MAGENTA}p1_pos [{self.p1_y}]")
		print(f"{MAGENTA}p2_pos [{self.p2_y}]")
		print(f"{MAGENTA}score_p1 [{self.score_p1}]")
		print(f"{MAGENTA}score_p2 [{self.score_p2}]")
		print(f"{MAGENTA}status [{self.status}]")
		print(f"{MAGENTA}map [{self.map}] {RESET}")