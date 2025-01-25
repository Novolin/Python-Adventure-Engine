# lmao i forgot to commit on my laptop so i dont want to have to manage all the dumb shit that comes with that



from collections import deque
import json

# Interface objects, for i/o


class TextInterface:
    # Parent class for text i/o interfaces
    def __init__(self, allcaps = False, limit_chars = False):
        self.allcaps = allcaps
        self.limit_chars = limit_chars
        self.last_player_input = None
        self.buffered_input_string = "" # in case it may come in pieces, like over UART or TTY or whatnot

    def write(self, text:str):
        # Writes the given string to the interface. 
        # Placeholder
        print(text)

    def prompt(self, prompt:str = ">"):
        # Prompt user for input 
        get_player_input = input(prompt)
        self.last_player_input = get_player_input
        return get_player_input

    def get_last_input(self):
        return self.last_player_input # this is less important on a 

class ConsoleInterface(TextInterface):
    def __init__(self):
        super().__init__()
        # placeholders are written to use the console so we are good to go!

class GameEvent:
    # This class defines text output events, as well as the effects they may have on other game objects
    def __init__(self, event_text, repeatable = True, target = False, effect = False):
        self.event_text = event_text
        self.repeatable = repeatable
        self.expired = False
        self.target = target
        self.effect = effect

    def fire_event(self, target_io):
        if self.repeatable or not self.expired:
            target_io.write(self.event_text) # the io system will handle if we do anything with cases or whatever
            if not self.repeatable:
                self.expired = True
        #TODO: If there's an effect, fire it here

class GameItem:
    def __init__(self, name:str, item_data):
        self.name = name
        self.alt_nouns = item_data["synonyms"]
        self.grabbable = item_data["grabbable"]
        self.look_event = None
        self.on_use = None

    def set_item_target(self, newTarget):
        self.target = newTarget

    def get_item_events(self):
        pass # would return the list of events 

    def get_item_names(self):
        namelist = [self.name]
        namelist.extend(self.alt_nouns)
        return namelist



class GameRoom: # Parent class for rooms in the game
    def __init__(self, room_name:str):
        self.name = room_name
        self.neighbors = {
            "N":{"open":None,"locked":None,"hidden":None}, 
            "S":{"open":None,"locked":None,"hidden":None}, 
            "E":{"open":None,"locked":None,"hidden":None}, 
            "W":{"open":None,"locked":None,"hidden":None}, 
            "U":{"open":None,"locked":None,"hidden":None}, 
            "D":{"open":None,"locked":None,"hidden":None}, 
            }
        self.items = {} # dict of items contained in the room
        self.events = {} # Dict of events which the room contains.

    def add_neighbor(self, neighbor, direction, state = "open", replace = False):
        # adds a neighbor room to the list of rooms
        if not self.neighbors[direction][state] or replace: # allow us to override if needed
            self.neighbors[direction][state] = neighbor
            return True
        return False # already taken!

    def add_event(self, event_name:str, event:GameEvent):
        self.events[event_name] = event
    
    def add_item(self, item_name:str, item:GameItem):
        self.items[item_name] = item

    def get_nouns(self):
        noun_list = {}
        for i in self.items:
            noun_list[i.name] = i
            if i.alt_nouns: # add refs for any alternate noun names we may have
                for n in i.alt_nouns:
                    noun_list[n] = i
        for n in self.neighbors:
            noun_list[n] = self.neighbors[n]["open"]






class GameParser:
    def __init__(self, iotarget:TextInterface):
        self.items = {}
        self.rooms = {}
        self.global_events = {}
        self.current_position = None
        self.inventory = []
        self.io = iotarget

    def load_game_data(self, data_file_path:str):
        self.io.write("Loading...\n")
        # load the data now lmao
        
        with open(data_file_path) as gamedata:
            for room in gamedata["rooms"]:
                self.rooms[room] = GameRoom(room)
                for contained_item in self.rooms[room]["items"]:
                    item_to_add = GameItem(contained_item) # LOGGING OFF HERE FOR TONIGHT MY BRAIN IS FRIEIEEIDID
                    # oh god i have to rewrite the item code 


        self.io.write("Complete!")





# Word - related stuff/global objects


VERB_TYPES = { # List of valid global verbs, and their synonyms.
    "move":["move", "go", "walk", "run", "enter"],
    "use":["use", "try", "insert", "open", "unlock"],
    "take":["take", "get", "grab", "pickup", "steal", "pick"],
    "look":["look", "examine", "see", "inspect", "observe", "peek", "check"]
}
DIRECTION_WORDS = {
    "U":["u","up", "higher"],
    "D":["d","down","lower"],
    "N":["n","north","nort"],
    "E":["e","east","est"],
    "W":["w","west","weast"],
    "S":["s", "south", "sout"]
}

# List of words the parser should ignore:
IGNORED_WORDS = ["on", "the", "to", "a"]

def get_synonym(word, room): # returns the appropriate synonym for a word. 
    if word.lower() in IGNORED_WORDS:
        return False # invalid word.
    for i in DIRECTION_WORDS:
        if word.lower() in DIRECTION_WORDS[i]:
            return i
    for i in room.items:
        if word in i.get_item_names():
            return i
    return False # no synonym found!

