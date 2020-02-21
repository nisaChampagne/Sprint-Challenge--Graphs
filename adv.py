from room import Room
from player import Player
from world import World
from util import Graph, Stack, Queue



import random
from ast import literal_eval

PURPLE = "\033[95m"
CYAN ="\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"
LIGHTRED     = "\033[91m"
LIGHTGREEN   = "\033[92m"
LIGHTYELLOW  = "\033[93m"
LIGHTBLUE    = "\033[94m"
LIGHTMAGENTA = "\033[95m"
LIGHTCYAN    = "\033[96m"
BACKGROUNDRED          = "\033[41m"
BACKGROUNDGREEN        = "\033[42m"
BACKGROUNDYELLOW       = "\033[43m"
BACKGROUNDBLUE         = "\033[44m"
BACKGROUNDMAGENTA      = "\033[45m"
BACKGROUNDCYAN         = "\033[46m"
BACKGROUNDLIGHTGRAY    = "\033[47m"
BACKGROUNDDARKGRAY     = "\033[100m"
BACKGROUNDLIGHTRED     = "\033[101m"
BACKGROUNDLIGHTGREEN   = "\033[102m"
BACKGROUNDLIGHTYELLOW  = "\033[103m"
BACKGROUNDLIGHTBLUE    = "\033[104m"
BACKGROUNDLIGHTMAGENTA = "\033[105m"
BACKGROUNDLIGHTCYAN    = "\033[106"

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
