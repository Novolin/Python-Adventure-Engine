# This file will load data from a json or w/e into a form the game can use

from engine import * # just do data types when youre not lazy

class GameDataLoader:
    def __init__(self):
        self.room_list = []
        self.item_list = []
        self.event_list = []
    def create_room(self, room_json):
        # Converts JSON-like data to a room object
        newRoom = GameRoom(room_json.name)
