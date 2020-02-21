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

# Load world
world = World()

'''

FROM READ ME:
You may find the commands `player.current_room.id`, 
`player.current_room.get_exits()`
 and `player.travel(direction)` useful.


 -relationship in current room provided tuple --> coordinates

I will start out  with the smallest map to make sure my traversal works

im thinking of having a util file with queue and stack available

maybe a traversal BFS as we don't have anything we are actively seeking out

possible game plan:
    1) populate graph by traversing through all the rooms

    2) keep track of rooms with directions

    3) call populate graph function (populate_graph())

    4) when length of visited is less than number of rooms:
        - find a path
        - traverse the returned list of moves
        -update current room
'''


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
print(PURPLE + f'1~~~~STARTING ROOM: {world.starting_room}')

map_graph = Graph()

#1) populate graph by traversing through all the rooms
def populate_map():
    #create a stack
    stack = Stack()
    #push starting room into stack
    stack.push(world.starting_room)
    #create empty set to hold visited
    visited = set()
    while stack.size() > 0:
        #pop out a room from stack
        room = stack.pop()
        print(RED + f'2~~~~ROOM: {room}')

        #variable name given to id of room
        room_id = room.id
        print(YELLOW + F"3~~~~~ROOM ID: {room_id}")

        #if room not in map
        if room_id not in map_graph.vertices:
            map_graph.add_vertex(room_id)

        #exits hold the directions, room.get_exits() comes from room model
        exits = room.get_exits()

        #loops through individual cardinal directions
        for direction in exits:
            print(GREEN + F"4~~~~~\n DIRECTIONS: {direction}")
            adjacent_room = room.get_room_in_direction(direction)
            print(BLUE + F"5~~~~\n ADJACENT ROOM: {adjacent_room}")
            adjacent_room_id = adjacent_room.id
            print(LIGHTCYAN + F"6~~~~\nADJACENT ROOM ID: {adjacent_room_id}")

            if adjacent_room_id not in map_graph.vertices:
                map_graph.add_vertex(adjacent_room_id)

            map_graph.add_edge(room_id, adjacent_room_id, direction)

            if adjacent_room_id not in visited:
                stack.push(adjacent_room)
        visited.add(room_id)
        print(LIGHTMAGENTA + f"7~~~~~\n VISITED: {visited}")

#2) keep track of rooms with directions , dead ends or not
def keep_track_of_room_directions(room_id, visited, map=map_graph):
    '''
    - will take in a room id and set of visited room ids
    - will return a set of moves that the player can take to get to closest space that hasnt been visited

    '''
    #create empty queue
    queue = Queue()
    # add a list with room_id and an empty list to the queue
    #will need 2 values for later
    queue.enqueue([[room_id], []])
    #empty set to hold rooms with moves
    rooms_with_moves = set()
    # add current room to set
    rooms_with_moves.add(room_id)
    print(LIGHTBLUE + F"8~~~~ROOM SET: {rooms_with_moves}")
    while queue.size() > 0:
        print(f"~~~~~~~~\n QUEUE: {queue}\n QUEUE SIZE: {queue.size()}")
        #grab off queue 2 values
        room, moves = queue.dequeue()
        #grabs last room id
        last_room_id = room[-1]
        print(LIGHTGREEN + F"9~~~~room: {room}, moves: {moves}")
        print(LIGHTCYAN + F"10~~~~LAST ROOM ID: {last_room_id}")

        #grab neighbors
        neighbors = map.get_neighbors(last_room_id)
        print(LIGHTMAGENTA + F"11~~~~~NEIGHBORS: {neighbors}")
        
        # copy of directions which are the keys
        copy_neighbors_keys = list(neighbors.keys())

        # dead end, return set of directions
        if len(copy_neighbors_keys) == 1 and neighbors[copy_neighbors_keys[0]] not in visited:
            dead_end = list(moves) + [copy_neighbors_keys[0]]
            print(RED + f"12~~~~DEAD END: {dead_end}")
            return dead_end

        else:
            #keep going
            for direction in neighbors:
                next_room = neighbors[direction]
                new_room = room + [next_room]
                new_moves = moves + [direction]
                print(YELLOW + F"13~~~~~~\nNEXT ROOM: {next_room}\n ROOM: {room}\n NEW ROOM: {new_room} \n NEW MOVES: {new_moves}")

                if next_room not in rooms_with_moves:
                    queue.enqueue([new_room, new_moves])
                    rooms_with_moves.add(next_room)
                    print(GREEN + f"14~~~~ \nROOM WITH MOVES: {rooms_with_moves}")
                if next_room not in visited:
                    return new_moves




populate_map()
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# empty set to store visited
visited = set()
#adding first rooms id to set
visited.add(world.starting_room.id)
#variable name given to first rooms id
current_room_id = world.starting_room.id
#total rooms
num_rooms = len(map_graph.vertices)

#4) when length of visited is less than number of rooms
while len(visited) < num_rooms:
    #grabbing moves from fn above
    moves = keep_track_of_room_directions(current_room_id, visited)
    #traverse the returned list of moves
    for direction in moves:
        #player method travel in that direction
        player.travel(direction)
        #append the direction to the path
        traversal_path.append(direction)
        #add the players current room id to visited set
        visited.add(player.current_room.id)
        print(BLUE + f"15~~~~~~\n VISITED: {visited}")

    #variable assigned to the players current room id 
    #-update current room
    current_room_id = player.current_room.id



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(LIGHTCYAN + f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print(LIGHTMAGENTA + "TESTS FAILED: INCOMPLETE TRAVERSAL")
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
