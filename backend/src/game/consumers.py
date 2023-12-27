import json
import asyncio
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Game, Player
from channels.db import database_sync_to_async
from django.db import transaction
from .pong import PongGame
from .tournament import Tournament
from .roomPong import RoomPong

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

class GameManager:
    _games = {}
    _tournament = {}

    @classmethod
    def get_game(cls, room_id):
        return cls._games.get(room_id)

    @classmethod
    def set_game(cls, room_id, game_instance):
        cls._games[room_id] = game_instance

    @classmethod
    def get_tournament(cls, room_id):
        return cls._tournament.get(room_id)
    
    @classmethod
    def set_tournament(cls, room_id, tournament):
        cls._tournament[room_id] = tournament



class RoomManager:
    _rooms = {}

    @classmethod
    def get_room(cls, room_id):
        return cls._rooms.get(room_id)
    
    @classmethod
    def set_room(cls, room_id, room_instance):
        cls._rooms[room_id] = room_instance




class GameConsumer(AsyncWebsocketConsumer):

    #-------------------------------------------------------------------------
    #                          CONNEXION functions
    #-------------------------------------------------------------------------
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.user = self.scope["user"]
        self.user_id = self.scope["user"].id
        self.username = self.scope["user"].username
        self.player = Player(self.user_id, self.username)
        self.slot = 0
        self.room = await self.get_room_instance()
        await asyncio.sleep(0.1)

        await self.accept()
        if not await self.checkIfAlreadyconneted():
            await self.close()
            return
        if not await self.checkRoomFull():
            await self.close()
            return
        
        if self.room.status == 'lobby':
            await self.handleNewUser()
        else:
            if not await self.reconnexion():
                return
        await self.send_player_info()
        await self.send_group_event('new_player_event', {})



    async def checkIfAlreadyconneted(self):
        if self.room.is_player_connected(self.player):
            await self.send(text_data=json.dumps({
                'error': "User is already connected"
            }))
            return False
        return True
    

    async def checkRoomFull(self):
        if self.room.room_is_full():
            await self.send(text_data=json.dumps({
                'error': "Room is full"
            }))
            print(f"{RED}Room {self.room_id} is full. {self.player.name} is rejected{RESET}")
            return False
        return True
    

    async def handleNewUser(self):
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        self.room.add_player_connected(self.player)
        self.slot = self.room.add_player_to_first_available_slot(self.player)

    async def reconnexion(self):
        self.slot = self.room.get_player_slot(self.player.user_id)
        if self.slot == None:
            await self.send(text_data=json.dumps({
                'error': "Room is full and game is already start"
            }))
            return False
        self.room.add_player_connected(self.player)
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        return True



    async def send_player_info(self):
        await self.send_event_to_current_client("player_info", {'name': self.player.name, 'slot': self.player.slot, 'is_master': self.player.isMaster})




    #-------------------------------------------------------------------------
    #                          DECONNEXION functions
    #-------------------------------------------------------------------------
    async def disconnect(self, close_code):
        if self.room.is_player_connected(self.player):
            if self.room.status == 'lobby':
                self.room.remove_player_connected(self.player)
            self.room.remove_player_slot(self.player)
            await self.channel_layer.group_discard(self.room_id, self.channel_name)
            await self.send_group_event('leave_player_event', {})





    #-------------------------------------------------------------------------
    #                          Room functions
    #-------------------------------------------------------------------------
    async def get_room_instance(self):
        room = RoomManager.get_room(self.room_id)
        if room == None:
            room_db = await self.get_room()
            room_instance = RoomPong(room_db)
            RoomManager.set_room(self.room_id, room_instance)
            room = RoomManager.get_room(self.room_id)
        await asyncio.sleep(0.1)
        return room
    

    #-------------------------------------------------------------------------
    #                       Send socket functions
    #-------------------------------------------------------------------------
    async def send_event_to_current_client(self, event_type, event_data):
        """
        Envoie un message personnalisé au client actuel.
        Args:
            event_type (str): Le type d'événement à envoyer.
            event_data (dict): Les données associées à l'événement.
        """
        message = {
            'type': event_type,
            'data': event_data,
        }
        await self.send(text_data=json.dumps(message))

    async def send_event_to_all_clients(self, event_type, event_data):
        message = {
            'type': event_type,
            'data': event_data,
        }
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'send.custom.message_handler',
                'message': message,
            }
        )

    async def send_custom_message_handler(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    

    

    #-------------------------------------------------------------------------
    #                          EVENT functions template
    #-------------------------------------------------------------------------

    async def send_group_event(self, event_type, event_data):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': event_type,
                **event_data,
            }
        )

    async def receive_group_event(self, event):
        event_type = event.get('type')
        if event_type:
            handler_name = f'receive_{event_type}'
            handler = getattr(self, handler_name, None)
            if handler and callable(handler):
                await handler(event)
            else:
                print(f"Aucun gestionnaire trouvé pour l'événement de type {event_type}")
        else:
            print("L'événement ne contient pas de type.")


    #-------------------------------------------------------------------------
    #                          BROADCAST functions
    #-------------------------------------------------------------------------

    async def new_player_event(self, event):
        await self.send_player_list_slot()
        await self.send_nb_player_connected()

    async def leave_player_event(self, event):
        await self.send_player_list_slot()
        await self.send_nb_player_connected()


    #-------------------------------------------------------------------------
    #                          BROADCAST clients functions
    #-------------------------------------------------------------------------

    async def send_player_list_slot(self):
        player_list = self.room.get_slot()
        formatted_player_list = []

        for slot, player in player_list.items():
            if player is not None:
                formatted_player_list.append({'slot': slot, 'name': player.name})
            else:
                formatted_player_list.append({'slot': slot, 'name': 'none'})

        await self.send_event_to_all_clients("player_list_slot", {'players': formatted_player_list})


    async def send_nb_player_connected(self):
        nbOfPlayer = len(self.room.get_connected_players())
        await self.send_event_to_all_clients("nb_players", {'nb_players': nbOfPlayer})

    async def send_change_screen(self, screen_type):
        await self.send_event_to_all_clients("change_screen", {'screen_type': screen_type})

    async def send_start_game(self):
        await self.send_event_to_all_clients("stat_game", {})

    async def send_game_state(self, game_state):
        await self.send_event_to_all_clients('game_update', game_state)
    
    async def send_end_single_game(self, game_state):
        await self.send_event_to_all_clients('game_end', game_state)




    #-------------------------------------------------------------------------
    #                          DATABASE functions
    #-------------------------------------------------------------------------
    @database_sync_to_async
    def get_room(self):
        try:
            return Room.objects.get(room_id=self.room_id)
        except Room.DoesNotExist:
            return None
        
    @database_sync_to_async
    def save_game_db(self, game_state):
        try:
            game = Game.objects.create(
                player1_id=game_state['p1_id'],
                player2_id=game_state['p2_id'],
                score_p1=game_state['p1_score'],
                score_p2=game_state['p2_score'],
                winner_id=game_state['winner_id'],
                loser_id=game_state['loser_id']
            )
            print(f"Game {game.game_id} saved in the database.")
        except Exception as e:
            print(f"Error saving game in the database: {e}")


    #-------------------------------------------------------------------------
    #                          INPUT functions
    #-------------------------------------------------------------------------
    #Function for receive data from client
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'keypress':
            key = data['key']
            # print(f"{self.player.name} press {key} in room {self.room_id}")
            await self.input_key(data['key'])
        
        if data['type'] == 'action':
           if data['data'] == 'startGame':
            await self.startGame()


    #-------------------------------------------------------------------------
    #                          STARTGAME functions
    #-------------------------------------------------------------------------
    async def checkIfGameIsReady(self):
        if not self.room.room_is_full():
            await self.send(text_data=json.dumps({
                'error': "Room is not full"
            }))
            return False
        return True

    
    async def startGame(self):
        if self.player.isMaster:
            if not await self.checkIfGameIsReady():
                return
            self.room.status = 'started'
            if self.room.is_local == True:
                print(f"{GREEN}Room [{self.room_id}] start a local game (in building){RESET}") 
            elif self.room.is_tournament == True:
                print(f"{GREEN}Room [{self.room_id}] start a tournament (in building){RESET}") 
            else:
                print(f"{GREEN}Room [{self.room_id}] start a single game{RESET}")
                await self.singleGameHandler()

    async def create_new_game(self, player1, player2):
        new_game = PongGame(self.room_id, player1, player2)
        GameManager.set_game(self.room_id, new_game)
        self.room.set_current_game(GameManager.get_game(self.room_id))



    async def singleGameHandler(self):
        player_1 = self.room.get_player_by_slot(1)
        player_2 = self.room.get_player_by_slot(2)
        await self.create_new_game(player_1, player_2)
        await self.send_change_screen('game')
        await self.send_start_game()
        self.game_task = asyncio.create_task(self.handleGameRun())



    #-------------------------------------------------------------------------
    #                          STARTGAME functions
    #-------------------------------------------------------------------------
    async def handleGameRun(self):
            game_state = self.room.current_game.update_game_state()
            while game_state['status'] == 'ongoing':
                self.game = GameManager.get_game(self.room_id)
                game_state = self.game.update_game_state()
                await self.send_game_state(game_state)
                await asyncio.sleep(0.1)
            if game_state['status'] == 'finished' and self.room.is_local == False:
                await self.save_game_db(game_state)
                await asyncio.sleep(0.1)
            await self.send_change_screen('end_game')
            await self.send_end_single_game(game_state)
            self.room.status = 'finished'
            await asyncio.sleep(0.1)
            if self.game_task:
                self.game_task.cancel()

            



    #-------------------------------------------------------------------------
    #                          ACTION functions
    #-------------------------------------------------------------------------
    async def input_key(self, key):
        if self.room.current_game != None:
            self.room.current_game.input_move(self.player.user_id, key)