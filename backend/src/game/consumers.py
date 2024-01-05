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
            await self.send_group_event('new_player_event', {})
        else:
            if not await self.reconnexion():
                await self.close()
                return
        await self.send_player_info()
        if self.room.is_local == True:
            await self.send_event_to_current_client('is_local', {})



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
        self.player = self.room.get_player_by_id(self.player.user_id)
        print(f"{GREEN}Reconnexion of {self.player.name}")
        self.room.add_player_connected(self.player)
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        return await self.handleReconnexionScreen()



    async def send_player_info(self):
        await self.send_event_to_current_client("player_info", {'name': self.player.name, 'slot': self.player.slot, 'is_master': self.player.isMaster})
    

    async def handleReconnexionScreen(self):
        if self.room.status == 'in_match':
            await self.send_change_screen('game')
            await self.send_start_game()
        elif self.room.status == 'waiting_next_macth':
            await self.send_change_screen('next_match')
            player_1, player_2 = self.room.current_tournament.get_players_for_next_match()
            await self.send_next_match_players(player_1, player_2)
        else:
            await self.send(text_data=json.dumps({
                'error': "All matches in this room are over"
            }))
            return False
        return True


            




    #-------------------------------------------------------------------------
    #                          DECONNEXION functions
    #-------------------------------------------------------------------------
    async def disconnect(self, close_code):
        if self.room.is_player_connected(self.player):
            if self.room.status == 'lobby':
                self.room.remove_player_slot(self.player)
            self.room.remove_player_connected(self.player)
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
    
    async def change_name_event(self, event):
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
    
    async def send_next_match_players(self, player1, player2):
        await self.send_event_to_all_clients('player_next_match', {'player_1': player1.name, 'player_2' : player2.name})

    async def send_end_game_tournament(self, game_state):
        await self.send_event_to_all_clients('game_end_tournament', game_state)
    
    async def send_end_tournament(self, winner_name, matches_list):
        await self.send_event_to_all_clients('tounrnament_end', {'winner': winner_name, 'matches_list': matches_list})


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

            elif data['data'] == 'startNextGame':
                await self.start_next_game()

            elif data['data'] == 'getNextGame':
                await self.get_next_game()

            elif data['data'] == 'changeName':
                await self.changeName(data['name'])
        if data['type'] == 'command':
            if data['command'] == 'player_speed':
                await self.set_player_speed(data['value'])
            elif data['command'] == 'score_max':
                await self.set_score_max(data['value'])
            elif data['command'] == 'timer':
                await self.set_timer(data['value'])
            elif data['command'] == 'ball_speed_x':
                await self.set_ball_speed_x(data['value'])
            else:
                await self.send_event_to_current_client('cli_log', {'message' : 'Invalid command. Please try again.'})



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
                await self.localGameHandler()
            elif self.room.is_tournament == True:
                print(f"{GREEN}Room [{self.room_id}] start a tournament{RESET}") 
                await self.startTournament()
            else:
                print(f"{GREEN}Room [{self.room_id}] start a single game{RESET}")
                await self.singleGameHandler()

    async def create_new_game(self, player1, player2):
        new_game = PongGame(self.room_id, player1, player2)
        new_game.update_game_value(self.room.player_speed, self.room.score_max, self.room.timer, self.room.ball_speed_x)

        GameManager.set_game(self.room_id, new_game)
        self.room.set_current_game(GameManager.get_game(self.room_id))

    async def create_new_local_game(self, player1, player2):
        new_game = PongGame(self.room_id, player1, player2, True)
        new_game.update_game_value(self.room.player_speed, self.room.score_max, self.room.timer, self.room.ball_speed_x)
        GameManager.set_game(self.room_id, new_game)
        self.room.set_current_game(GameManager.get_game(self.room_id))



    async def singleGameHandler(self):
        player_1 = self.room.get_player_by_slot(1)
        player_2 = self.room.get_player_by_slot(2)
        await self.create_new_game(player_1, player_2)
        await self.send_change_screen('game')
        await asyncio.sleep(0.1)
        await self.send_start_game()
        await asyncio.sleep(0.1)
        self.game_task = asyncio.create_task(self.handleGameRun())

    async def localGameHandler(self):
        player = self.room.get_player_by_slot(1)
        player_1 = Player(player.user_id, 'player 1')
        player_2 = Player(player.user_id, 'player 2')
        player_1.slot = player.slot
        player_2.slot = player.slot
        await self.create_new_local_game(player_1, player_2)
        await self.send_change_screen('game')
        await asyncio.sleep(0.1)
        await self.send_start_game()
        await asyncio.sleep(0.1)
        self.game_task = asyncio.create_task(self.handleGameRun())




    #-------------------------------------------------------------------------
    #                          STARTGAME functions
    #-------------------------------------------------------------------------
    async def handleGameRun(self):
            self.room.status = 'in_match'
            game_state = self.room.current_game.update_game_state()
            while game_state['status'] == 'ongoing':
                self.game = GameManager.get_game(self.room_id)
                game_state = self.game.update_game_state()
                await self.send_game_state(game_state)
                await asyncio.sleep(0.02)

            #save the game if not local
            if game_state['status'] == 'finished' and self.room.is_local == False:
                await self.save_game_db(game_state)
                await asyncio.sleep(0.1)

            print(f"{MAGENTA} IS TOURNAMENT = {self.room.is_tournament} {RESET}")
            print(f"{MAGENTA} status = {game_state['status']} {RESET}")
            #end single game if not tournament
            if game_state['status'] == 'finished' and self.room.is_tournament == False:
                await self.send_change_screen('end_game')
                await self.send_end_single_game(game_state)
                self.room.status = 'finished'
                await asyncio.sleep(0.1)
            
            #end tournaement
            elif game_state['status'] == 'finished' and self.room.is_tournament == True:
                self.room.current_tournament.save_and_set_next_mach(game_state['winner_name'], game_state['loser_name'])
                await asyncio.sleep(0.1)
                if self.room.current_tournament.finished == False:
                    print(f"{MAGENTA} Send End Match {RESET}")
                    await self.send_change_screen('end_game_tournament')
                    await self.send_end_game_tournament(game_state)
                    self.room.status = 'waiting_next_macth'
                else:
                    print(f"{MAGENTA} Send End Tournament {RESET}")
                    matches_list = self.room.current_tournament.get_matches_list()
                    winner_name = self.room.current_tournament.winner
                    await self.send_change_screen('end_tournament')
                    await self.send_end_tournament(winner_name, matches_list)
                    self.room.status = 'finished_tournament'
            time.sleep(1)
            if self.game_task:
                self.game_task.cancel()

            



    #-------------------------------------------------------------------------
    #                          ACTION functions
    #-------------------------------------------------------------------------
    async def input_key(self, key):
        if self.room.current_game != None:
            self.room.current_game.input_move(self.player.user_id, key)

    async def changeName(self, name):
        if self.room.change_player_name(self.player.user_id, name):
            self.player.name = name
            await self.send_player_info()
            await self.send_group_event('change_name_event', {})
        else:
            await self.send_event_to_current_client("name_already_use", {'name': name})



    #-------------------------------------------------------------------------
    #                          Tournament functions
    #-------------------------------------------------------------------------
    
    async def tournamentGameHandler(self, player_1, player_2):
        await self.create_new_game(player_1, player_2)
        await self.send_change_screen('game')
        await asyncio.sleep(0.1)
        await self.send_start_game()
        await asyncio.sleep(0.1)
        self.game_task = asyncio.create_task(self.handleGameRun())


    async def create_tournament(self):
        tournament_instance = Tournament(self.room.connected_players)
        GameManager.set_tournament(self.room_id, tournament_instance)
        self.room.current_tournament = GameManager.get_tournament(self.room_id)

    async def startTournament(self):
        self.room.status = 'waiting_next_macth'
        await self.create_tournament()
        player_1, player_2 = self.room.current_tournament.get_players_for_next_match()
        print(f'{MAGENTA}Players for next match: {player_1.name, player_2.name}{RESET}')
        await self.send_change_screen('next_match')
        await self.send_next_match_players(player_1, player_2)

    
    async def start_next_game(self):
        print(f"{MAGENTA}Start Next Game event received {RESET}")
        player_1, player_2 = self.room.current_tournament.get_players_for_next_match()
        await self.tournamentGameHandler(player_1, player_2)

    async def get_next_game(self):
        player_1, player_2 = self.room.current_tournament.get_players_for_next_match()
        await self.send_change_screen('next_match')
        await self.send_next_match_players(player_1, player_2)



    #-------------------------------------------------------------------------
    #                          CLI functions
    #-------------------------------------------------------------------------
    

    async def set_player_speed(self, value):
        room = RoomManager.get_room(self.room_id)
        try :
            value = float(value)
        except  ValueError:
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a number between 1 and 3. Please try again'})
            return
        if value < 1 or value > 3 :
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a number between 1 and 3. Please try again'})
        else :
            room.player_speed = value
            await self.send_event_to_current_client('cli_log', {'message' : 'Player speed update success'})


    async def set_score_max(self, value):
        room = RoomManager.get_room(self.room_id)
        try :
            value = int(value)
        except  ValueError:
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a numbre between 1 and 50. Please try again'})
            return
        if value < 1 or value > 50:
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a numbre between 1 and 50. Please try again'})
        else :
            room.score_max = value
            await self.send_event_to_current_client('cli_log', {'message' : 'Score max update success'})



    async def set_timer(self, value):
        room = RoomManager.get_room(self.room_id)
        try :
            value = int(value)
        except  ValueError:
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a numbre between 1 and 100. Please try again'})
            return
        if value < 1 or value > 100:
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a numbre between 1 and 100. Please try again'})
        else :
            room.timer = value
            await self.send_event_to_current_client('cli_log', {'message' : 'Timer update success'})
    


    async def set_ball_speed_x(self, value):
        room = RoomManager.get_room(self.room_id)
        try :
            value = float(value)
        except  ValueError:
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a float between 0.1 and 0.3. Please try again'})
            return
        if value < 0.1 or value > 0.3 :
            await self.send_event_to_current_client('cli_log', {'message' : 'Invalid value: Must be a float between 0.1 and 0.3. Please try again'})
        else :
            room.ball_speed_x = value
            await self.send_event_to_current_client('cli_log', {'message' : 'Ball Speed X update success'})
        
