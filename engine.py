# V0.0.1 - super super super early

from collections import deque

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

class GameEvent:
    # This class defines text output events, as well as the effects they may have on other game objects
    def __init__(self, event_text, event_trigger, repeatable = True, required_item = None, effect = None):
        self.event_text = event_text
        self.trigger = event_trigger
        self.repeatable = repeatable
        self.required_item = required_item # May be room or item
        self.effect = effect
        self.expired = False

    def fire_event(self):
        if not self.repeatable:
            self.expired = True
        
        if self.effect:
            # Execute any changes to the target here
            pass
        return self.event_text 


class GameItem:
    def __init__(self, item_name:str, item_alt_names:list = [], target = None, grabbable = False):
        self.name = item_name
        self.alt_nouns = item_alt_names
        self.target = target
        self.grabbable = grabbable
        self.look_event = None
        self.on_use = None

    def set_item_target(self, newTarget):
        self.target = newTarget

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
        self.items = []
        self.events = []
        self.enter_event = None
        self.look_event = None

    def load_room_data(self, data_as_obj):
        # Interprets a loaded json object dealio and makes it the room.
        pass

    def add_neighbor(self, neighbor, direction, state = "open"):
        # adds a neighbor room to the list of rooms
        if not self.neighbors[direction][state]:
            self.neighbors[direction][state] = neighbor
            return True
        return False # already taken!

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
    # object to handle string decoding
    def __init__(self, input_handler:TextInterface, start_room = 0, start_inventory = []):
        self.current_room = start_room # What room are we starting the game in
        self.current_items = start_inventory # Items we have in our starting inventory
        self.event_queue = deque((), 16) # List of events that need to be fired.
        self.io = input_handler
        # This is probaly not the most efficient way, but i think memory for text is so small i can get away with it.
        self.room_list = [] # All rooms in the game
        self.item_list = [] # all items in the game

    def get_allowed_nouns(self):
        # returns a dict of allowed words
        allowed_words = {"rooms":[], "items":[]}
        allowed_words.extend(self.current_room.get_nouns())
        for i in self.current_items:
            allowed_words.append(i.get_nouns())
        
    def parse_incoming_string(self, string_to_parse): 
        # Returns a tuple of (verb, object 1, object 2)
        # Verb is the action to do to/with the given objects
        # Object 2 is the target of the action, and may be None.
        # Examples: ("use", "key", "door"), ("move", "player", "north"), ("look", "room", None)
        output = [None, None, None]
        nouns = self.get_allowed_nouns()
        word_list = string_to_parse.split()

        if word_list[0] in VERB_TYPES["move"]:
            output[0] = "move"
            output[1] = "player"
            can_move = False
            next_word = 0
            while not can_move:
                next_word += 1
                if next_word >= len(word_list):
                    # We haven't found a match.
                    break
                can_move = get_synonym(word_list[next_word], self.room)
            output[2] = can_move 
        else:
            print("NOT READY TO DO THAT YET")
        return output

    def execute_parsed_cmd(self, parse_list:list):
        if parse_list[0] == "move":
            print("I WOULD DO A MOVE HERE!")



    def parse_loop(self, input_source):
        # this is where we would load data
        next_string = "starting....."
        while True:
            print(next_string)
            if input_source == "console":
                parsed = self.parse_incoming_string(input("ENTER COMMAND> "))
                if parsed[0] == "move":
                    print("ASS")



    