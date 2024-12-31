# V0.0.1 - super super super early


# Not even bothering to import anything yet since idk what I'll need

VERB_TYPES = { # List of valid global verbs, and their synonyms.
    "move":["move", "go", "walk", "run", "enter"],
    "use":["use", "try", "insert", "open", "unlock"],
    "take":["take", "get", "grab", "pickup", "steal"],
    "look":["look", "examine", "see", "inspect", "observe", "peek", "check"]
}
# List of words the parser should ignore:
IGNORED_WORDS = ["on", "the", "to"]

class GameParser:
    # object to handle string decoding
    def __init__(self, start_room = 0, start_inventory = []):
        self.current_room = start_room # What room are we starting the game in
        self.current_items = start_inventory # Items we have in our starting inventory
        
    def parse_incoming_string(self, string_to_parse): 
        # Returns a tuple of (verb, object 1, object 2)
        # Verb is the action to do to/with the given objects
        # Object 2 is the target of the action, and may be None.
        # Examples: ("use", "key", "door"), ("move", "player", "north"), ("look", "room", None)
        output = [None, None, None]
        listed_words = string_to_parse.split() # Split the string into separate words
        check_word = 0
        while check_word < len(listed_words): # roughing it out with a while loop
            if listed_words[check_word] in IGNORED_WORDS: # we don't need that
                check_word += 1
                continue 
            if listed_words[check_word] in VERB_TYPES["look"]: # We are looking at an object
                if output[0] == None:
                    output[0] = "look"
                check_word += 1
                continue
            if listed_words[check_word] in VERB_TYPES["take"]: # We are taking an object
                