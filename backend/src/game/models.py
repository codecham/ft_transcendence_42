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
	score_p1 = models.PositiveIntegerField(default=0)
	score_p2 = models.PositiveBigIntegerField(default=0)
	winner_id = models.PositiveBigIntegerField(default=0)
	loser_id = models.PositiveBigIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Room(models.Model):
	room_id = models.AutoField(primary_key=True)
	creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	max_player = models.PositiveIntegerField()
	is_tournament = models.BooleanField(default=False)
	is_local = models.BooleanField(default=False)



class Player:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.slot = 0
        self.isMaster = False
