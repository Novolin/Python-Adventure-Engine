# V0.0.1 - super super super early


# Not even bothering to import anything yet since idk what I'll need

VERB_TYPES = { # List of valid global verbs, and their synonyms.
    "move":["move", "go", "walk", "run", "enter"],
    "use":["use", "try", "insert", "open", "unlock"],
    "take":["take", "get", "grab", "pickup", "steal", "pick"],
    "look":["look", "examine", "see", "inspect", "observe", "peek", "check"]
}
GLOBAL_VERB_LIST = [] # list of verbs that will always be available
for word in VERB_TYPES:
    GLOBAL_VERB_LIST.extend(VERB_TYPES[word])
# List of words the parser should ignore:
IGNORED_WORDS = ["on", "the", "to"]

class GameEvent:
    # This class defines text output events, as well as the effects they may have on other game objects
    def __init__(self, event_text, repeatable = True, target = None, effect = None):
        self.event_text = event_text
        self.repeatable = repeatable
        self.target = target # May be room or item
        self.effect = effect
        self.expired = False

    def fire_event(self):
        if not self.repeatable:
            self.expired = True
        
        if self.target:
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

    def get_item_events(self):
        pass # would return the list of events 



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
        self.enter_event = None
        self.look_event = None

    def add_neighbor(self, neighbor, direction, state = "open"):
        # adds a neighbor room to the list of rooms
        if not self.neighbors[direction][state]:
            self.neighbors[direction][state] = neighbor
            return
        print("{direction} neighbor slot in {neighbor} already filled.")
        raise ValueError

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
    def __init__(self, start_room = 0, start_inventory = []):
        self.current_room = start_room # What room are we starting the game in
        self.current_items = start_inventory # Items we have in our starting inventory
        

    def get_allowed_nouns(self):
        # returns a list of allowed words
        allowed_words = []
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
        if word_list[1] in VERB_TYPES["move"]:
            print("MOVE")
        elif word_list[1] in VERB_TYPES["look"]:
            print("LOOK")
        elif word_list[1] in VERB_TYPES["take"]:
            print("TAKE")
        elif word_list[1] in VERB_TYPES["use"]:
            print("USE")



