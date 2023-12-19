import json
import asyncio
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Player, Game
from channels.db import database_sync_to_async
from django.db import transaction
from .pong import PongGame

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

    @classmethod
    def get_game(cls, room_id):
        return cls._games.get(room_id)

    @classmethod
    def set_game(cls, room_id, game_instance):
        cls._games[room_id] = game_instance





class GameConsumer(AsyncWebsocketConsumer):

    #-------------------------------------------------------------------------
    #                          CONNEXION functions
    #-------------------------------------------------------------------------
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room = await self.get_room()
        self.user = self.scope["user"]
        self.user_id = self.scope["user"].id
        self.username = self.scope["user"].username
        self.game = None


        await self.accept()
        if not await self.checkRoomIdConnection(self.username):
            return

        self.isMaster = False
        self.game_started = await self.get_game_start()
        self.isTournament = await self.get_is_tournament()
        self.slot = 0
        await asyncio.sleep(0.1)

        if not self.game_started:
            await self.handleNewUser()
            await self.send_information_to_new_client()
        elif await self.player_is_in_slot():
            await self.handleReconnexion()
            await self.send_information_to_new_client()
        else:
            await self.send(text_data=json.dumps({
                'error': "Game already start"
            }))
            await self.close()
        




    async def checkRoomIdConnection(self, username):
        #Handle error room
        if not self.room:
            print(f"{RED}Room_id [[{self.room_id}]] doens't exist. [{username}]'s socket closed{RESET}")
            await self.send(text_data=json.dumps({
                'error': "Room doesn't exist"
            }))
            await self.close()
            return False
        return True
    

    async def is_user_already_connected(self):
        connected_users = await self.get_connected_players()
        return self.username in connected_users



    async def handleNewUser(self):
        # Add user to group
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        # Add user to player slot
        await self.add_user_to_slot()
        # Add user to connected players
        await self.add_user_from_players_connected()
        # Add player to master
        if not await self.has_master_player():
            await self.set_master_for_player()
            self.isMaster = True
        elif self.room.master_user_id == self.user_id:
            self.isMaster = True
        # Get Room Creator
        self.room_creator = await database_sync_to_async(lambda: self.room.creator.username)()
        # Get Player Slot
        self.player_slot = await self.get_player_slots()
        # Get Connected user
        self.connected_player = await self.get_connected_players()
        # Get Max Player
        self.max_player = self.room.max_player
        # Get Player Object
        self.player = await self.get_player_by_id()
        #Print Player log join
        print(f"{GREEN}Room [{self.room_id}]: new player join: {self.username}{RESET}")
        # Broadcast to users in group
        await self.send_group_event('user.joined', {})


    async def handleReconnexion(self):
        self.player = await self.get_player_by_id()
        self.player_slot = await self.get_player_slots()
        await self.set_player_connexion(True)
        await asyncio.sleep(0.1)
        self.slot = self.player.slot
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        if self.room.master_user_id == self.user_id:
            self.isMaster = True
        self.connected_player = await self.get_connected_players()
        self.max_player = self.room.max_player
        self.game = GameManager.get_game(self.room_id)
        print(f"{GREEN}Room [{self.room_id}]: player reconnexion: {self.username}{RESET}")
        await self.send(text_data=json.dumps({
                'type': 'game_start',
            }))
        await self.send_group_event('user.reconnexion', {})

    

    async def send_information_to_new_client(self):

        #Send name
        await self.send(text_data=json.dumps({
            'type': 'name',
            'name': self.username 
        }))

        #Send information of player
        await self.send(text_data=json.dumps({
            'type': 'player_info',
            'name': self.username,
            'slot' : self.slot,
            'is_master': self.isMaster
        }))



    #-------------------------------------------------------------------------
    #                          DECONNEXION functions
    #-------------------------------------------------------------------------
    async def disconnect(self, close_code):
        if self.room:
            if not self.game_started:
                #Remove user from connected player
                await self.remove_user_from_players_connected()
                #Remove user from player slot
                await self.remove_user_to_slot()
                #Remove master player
                await self.remove_player_master()
                #Broadcast user left
                await self.send_group_event('user.left', {})
                #Remove user form group layer
                await self.channel_layer.group_discard(self.room_id, self.channel_name)
                #Print the player list
                await self.print_connected_players()
                print(f"{RED}{self.username} leave room {self.room_id}{RESET}")
            else:
                #Remove user from connected player
                await self.set_player_connexion(False)
                await self.channel_layer.group_discard(self.room_id, self.channel_name)
                await self.send_group_event('user_deconnexion', {})
                print(f"{RED}{self.username} deconnexion in room {self.room_id}{RESET}")



    #-------------------------------------------------------------------------
    #                          BROADCAST functions
    #-------------------------------------------------------------------------
    #Function for send message to all user in the same groupe
    async def send_group_message(self, message):
        await self.channel_layer.group_send(
            self.room_id,
            message
        )
    
    async def send_connected_players(self):
        await self.send_group_message({
            'type': 'users_list',
            'users_list': self.connected_player,
            'max_player': self.max_player,
        })

    async def users_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'users_list',
            'users_list': self.connected_player,
            'max_player': self.max_player,
        }))

    async def send_game_started(self):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'game_start',
            }
        )
    
    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_start',
        }))
    

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'data': event['data'],
        }))


    #-------------------------------------------------------------------------
    #                          EVENT functions template
    #-------------------------------------------------------------------------

    async def send_group_event(self, event_type, event_data):
        """
        Envoie un événement à tous les utilisateurs du groupe.
        Args:
            event_type (str): Le type d'événement à envoyer.
            event_data (dict): Les données associées à l'événement.
        """
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': event_type,
                **event_data,
            }
        )

    async def receive_group_event(self, event):
        """
        Gère la réception d'un événement de groupe.
        Args:
            event (dict): Les données de l'événement reçu.
        """
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
    #                          EVENT functions
    #-------------------------------------------------------------------------



    async def user_joined(self, event):
        self.room = await self.get_room()
        await asyncio.sleep(0.1)
        self.connected_player = await self.get_connected_players()
        self.player_slot = await self.get_player_slots()
        await self.send_connected_players()
        await self.log_room()

    async def user_left(self, event):
        self.room = await self.get_room()
        await asyncio.sleep(0.1)
        self.connected_player = await self.get_connected_players()
        self.player_slot = await self.get_player_slots()
        await self.send_connected_players()
        await self.log_room()

    async def user_reconnexion(self, event):
        self.room = await self.get_room()
        await asyncio.sleep(0.1)
        self.connected_player = await self.get_connected_players()
        await self.send_connected_players()

    
    async def user_deconnexion(self, event):
        self.room = await self.get_room()
        await asyncio.sleep(0.1)
        self.connected_player = await self.get_connected_players()
        await self.send_connected_players()


    async def game_start_event(self, event):
        self.room = await self.get_room()
        self.game_started = True
        await self.send_game_started()

    async def share_game_instance(self, event):
        self.room = await self.get_room()
        self.game = GameManager.get_game(self.room_id)
        await asyncio.sleep(0.1)





    #-------------------------------------------------------------------------
    #                          INPUT functions
    #-------------------------------------------------------------------------
    #Function for receive data from client
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'keypress':
            key = data['key']
            username = self.scope['user'].username
            print(f"{username} press {key} in room {self.room_id}")
            await self.input_key(data['key'])
        
        if data['type'] == 'action':
           if data['data'] == 'startGame':
            await self.startGame()





    #-------------------------------------------------------------------------
    #                          PRINT functions
    #-------------------------------------------------------------------------
    #Print the list of connected users
    async def print_connected_players(self):
        connected_players = await self.get_connected_players()
        print(f"{CYAN}Players connected in room [{self.room_id}]: {connected_players}{RESET}")



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
    def add_user_from_players_connected(self):
        player, created = Player.objects.get_or_create(user=self.user, name=self.username, room_id=self.room_id, slot=self.slot)
        self.room.add_user_to_players_connected(player)

    @database_sync_to_async
    def remove_user_from_players_connected(self):
        self.room.remove_user_from_players_connected(self.user, self.slot)
    
    @database_sync_to_async
    def get_connected_players(self):
        list_of_player = self.room.get_connected_players()
        return list_of_player
    
    @database_sync_to_async
    def add_user_to_slot(self):
        with transaction.atomic():
            self.slot = self.room.add_user_to_slot(self.user.id)
            
    
    @database_sync_to_async
    def remove_user_to_slot(self):
        with transaction.atomic():
            self.room.remove_user_from_slot(self.user.id)

    @database_sync_to_async
    def get_player_slots(self):
        with transaction.atomic():
            player_slots = self.room.get_player_slots()
            return player_slots
    
    @database_sync_to_async
    def log_db(self):
        self.room.print_value_db()
    
    @database_sync_to_async
    def get_max_player(self):
        self.room.get_max_player()
    
    @database_sync_to_async
    def has_master_player(self):
        return self.room.has_master_player()
    
    @database_sync_to_async
    def get_player_by_id(self):
        return self.room.get_player_by_user_id(self.user_id)
    
    @database_sync_to_async
    def set_master_for_player(self):
        self.room.set_user_master(self.user_id)

    @database_sync_to_async
    def remove_player_master(self):
        self.room.remove_master(self.user_id)

    @database_sync_to_async
    def get_number_of_player_connected(self):
        return self.room.get_number_of_players_connected()
    
    @database_sync_to_async
    def set_game_start(self, value):
        self.room.set_game_start(value)
    
    @database_sync_to_async
    def get_game_start(self):
        return self.room.get_game_start()
    
    @database_sync_to_async
    def get_is_tournament(self):
        return self.room.get_is_tournament()
    
    @database_sync_to_async
    def player_is_in_slot(self):
        return self.room.player_is_in_slot(self.user_id)
    
    @database_sync_to_async
    def set_player_connexion(self, value):
        self.room.set_player_connexion(self.user_id, value)
    
    @database_sync_to_async
    def get_player_by_slots(self, slot):
        return self.room.get_player_by_slot(slot)
    
    @database_sync_to_async
    def create_game_db(self, player1_id, player2_id):
        new_game = Game.objects.create(player1_id=player1_id, player2_id=player2_id, status='ongoing')
        return new_game
    
    @database_sync_to_async
    def set_current_game(self, game_id):
        self.room.set_current_game(game_id)

    
    async def log_room(self):
        print(f"{CYAN}Log of room [{self.room_id}] for user [{self.username}] connected on slot [{self.slot}] {RESET}")
        print(f"{CYAN}Connected_user [{self.connected_player}]{RESET}")
        print(f"{CYAN}Player Slot [{self.player_slot}]{RESET}")



    #-------------------------------------------------------------------------
    #                          BROADCAST GAME functions
    #-------------------------------------------------------------------------

    #event for game_start
    async def send_event_start_game(self):
        await self.send(text_data=json.dumps({
                'type': 'game_start',
            }))

        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'game_start',
            }
        )

    #event for game_update
    async def send_event_game_update(self, room_id, game_state):
        print(f"{room_id} send game_state: {game_state}")
        await self.channel_layer.group_send(
            room_id,
            {
                'type': 'game_update',
                'data': game_state,
            }
        )
        await asyncio.sleep(0.1)


    
    #-------------------------------------------------------------------------
    #                          GAME functions
    #-------------------------------------------------------------------------

    #handle error before start
    async def handleNewGameError(self):
        nbPlayer = await self.get_number_of_player_connected()
        await asyncio.sleep(0.1)
        if self.isMaster == False:
            print(f"{RED}{self.username}: Only Master can start game (master-id = [{self.room.master_user_id}]){RESET}")
            return False
        if nbPlayer < self.room.max_player:
            print(f"{RED}{self.username}: Room is not full{RESET}")
            return False
        return True
    

    #create a game instance with game manager
    async def createGameInstance(self):
        game_instance = PongGame(self.room_id, self.game_info)
        GameManager.set_game(self.room_id, game_instance)
        self.game = game_instance


    #Create a new game in db
    async def create_new_game_db(self, slot1, slot2):
        p1_id = self.player_slot[slot1] 
        p2_id = self.player_slot[slot2] 
        new_game = await self.create_game_db(p1_id, p2_id)
        self.game_info = new_game
    

    async def handleGameRun(self):
        game_state = self.game.update_game_state()
        print(f"game_state; {game_state}")
        while game_state['status'] != 'finished':
            self.game = GameManager.get_game(self.room_id)
            game_state = self.game.update_game_state()
            await self.send(text_data=json.dumps({
                'type': 'game_update',
                'data': game_state,
            }))
            await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': 'game_update',
                    'data': game_state,
                })
            await asyncio.sleep(0.1)
        await self.send(text_data=json.dumps({
                'type': 'game_update',
                'data': game_state,
            }))
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'game_update',
                'data': game_state,
            })


    async def create_new_game(self, p1_slot, p2_slot):
        #create a game in db:
        await self.create_new_game_db(p1_slot, p2_slot)
        #create a game instance:
        await self.createGameInstance()
        #share game instance to all players
        await self.send_group_event('share_game_instance', {})

    
    async def start_new_game(self):
        await self.set_game_start(True)
        self.game_started = True
        await self.send_game_started()
        await self.set_current_game(self.game_info.game_id)
        await self.send_event_start_game()
        await self.send_group_event('game_start_event', {})
        await asyncio.sleep(0.1)
        asyncio.create_task(self.handleGameRun())




    async def startGame(self):
        if not await self.handleNewGameError():
            return
        if self.room.is_tournament == False:
            await self.create_new_game('1', '2')
            await self.start_new_game()
        else:
            #lauch tournament
            print(f"{GREEN}{self.username}: lauch tournament {RESET}")
        



    #-------------------------------------------------------------------------
    #                          ACTION functions
    #-------------------------------------------------------------------------

    async def input_key(self, key):
        if self.game != None:
            user_id = self.scope['user'].id
            self.game.input_move(user_id, key)