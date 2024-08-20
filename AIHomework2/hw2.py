import collections, fileinput
from typing import Protocol, Iterator, Tuple, TypeVar, Optional

T = TypeVar('T')

#All of these implementations were created by Red Blob Games
#My code starts at line 225.
Location = TypeVar('Location')
class Graph(Protocol):
    def neighbors(self, id: Location) -> list[Location]: pass

class SimpleGraph:
    def __init__(self):
        self.edges: dict[Location, list[Location]] = {}
    
    def neighbors(self, id: Location) -> list[Location]:
        return self.edges[id]

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: T):
        self.elements.append(x)
    
    def get(self) -> T:
        return self.elements.popleft()

# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " S "
    if 'goal' in style and id == style['goal']:   r = " G "
    if id in graph.walls: r = "###"
    return r

def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)

GridLocation = Tuple[int, int]

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []
    
    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}
    
    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]

# thanks to @m1sp <Jaiden Mispy> for this simpler version of
# reconstruct_path that doesn't have duplicate entries

def reconstruct_path(came_from: dict[Location, Location],
                     start: Location, goal: Location) -> list[Location]:

    current: Location = goal
    path: list[Location] = []
    if goal not in came_from: # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path


def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

class SquareGridNeighborOrder(SquareGrid):
    def neighbors(self, id):
        (x, y) = id
        neighbors = [(x + dx, y + dy) for (dx, dy) in self.NEIGHBOR_ORDER]
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return list(results)

def test_with_custom_order(neighbor_order):
    if neighbor_order:
        g = SquareGridNeighborOrder(30, 15)
        g.NEIGHBOR_ORDER = neighbor_order
    else:
        g = SquareGrid(30, 15)
    g.walls = DIAGRAM1_WALLS
    start, goal = (8, 7), (27, 2)
    came_from = breadth_first_search(g, start, goal)
    draw_grid(g, path=reconstruct_path(came_from, start=start, goal=goal),
              point_to=came_from, start=start, goal=goal)

class GridWithAdjustedWeights(GridWithWeights):
    def cost(self, from_node, to_node):
        prev_cost = super().cost(from_node, to_node)
        nudge = 0
        (x1, y1) = from_node
        (x2, y2) = to_node
        if (x1 + y1) % 2 == 0 and x2 != x1: nudge = 1
        if (x1 + y1) % 2 == 1 and y2 != y1: nudge = 1
        return prev_cost + 0.001 * nudge

#def depth_first_search(graph: Graph, start: Location):
 #   frontier = Queue()
  #  frontier.put(start)
   # came_from: dict[Location, Optional[Location]] = {}
    #came_from[start] = None
    
    #while not frontier.empty():
     #   current: Location = frontier.get()
        
      #  if current == goal:
       #     break
        
        #for next in graph.neighbors(current):
         #   if next not in came_from:
          #      frontier.put(next)
           #     came_from[next] = current
    
    #return came_from

def breadth_first_search(graph: Graph, start: Location, goal: Location):
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    
    return came_from

def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

#This is where my code starts---------------------------------------------------------

#It asks for the name of .txt file to test and opens it in read mode.
userInput = input("Enter the file name:")
mazeFile = open(userInput, "r")
#Creates a list containing the lines of the file.
Lines = mazeFile.readlines()

#Loops through the list and counts how many lines it has.
count = 0
for line in Lines:
    count+=1
    print(line.strip())

print("\n")


a=0
walls = []
start = (0, 0)
goal = (0, 0)

#Loops through all the characters in each line to identify the
#type of character. It assigns an index value each one. It
#then appends the corresponding wall characters to a list, and
#the start and goal values are saved.
for x in range(len(Lines)):
    a = str(Lines[x])
    for i in range(len(a)):
        if a[i] == '%':
            indexx = i
            indexy = x
            walls.append((indexx, indexy))
        if a[i] == 'S':
            start = (i, x)
        if a[i] == 'G':
            goal = (i, x)
        i = i + 1

#Prints the size of the maze, and the coordinates for the start and goal.
print("Size of maze: ",len(Lines),"x",len(a))
print("Location for start:",start, "\nLocation for goal:",goal)           

type = input("\nEnter 'astar', 'greedy':")
if type == "astar":
    #Creates a grid for the A* algorithm using previously obtained values.
    maze = GridWithWeights(len(a), len(Lines))
    maze.walls = walls
    #maze.weights = {loc: 5 for loc in [(3, 4)]}

    #Prints the A* search path, and the best path to take.
    print("\nA* search:")
    start, goal = start, goal
    came_from, cost_so_far = a_star_search(maze, start, goal)
    draw_grid(maze, point_to=came_from, start=start, goal=goal)
    print()
    draw_grid(maze, path=reconstruct_path(came_from, start=start, goal=goal))


    mazeFile.close()

#I can't get depth first search to work properly.
#print("\nDepth First Search:")
#maze = GridWithWeights(len(a), len(Lines))
#maze.walls = walls
#start = start
#parents = depth_first_search(maze, start)
#draw_grid(maze, point_to=parents, start=start)
#draw_grid(maze, path=reconstruct_path(came_from, start=start, goal=goal))

if type == "greedy":
    #Prints the Greedy Best First Search path.
    print("\nGreedy Best First Search:")
    maze = SquareGrid(len(a), len(Lines))
    maze.walls = walls
    start, goal = start, goal
    came_from = breadth_first_search(maze, start=start, goal=goal)
    parents = breadth_first_search(maze, start, goal)
    draw_grid(maze, point_to=parents, start=start, goal=goal)
    draw_grid(maze, path=reconstruct_path(came_from, start=start, goal=goal))

    mazeFile.close()


#print("\n")

#for line in fileinput.input("maze1.txt"):
#    if 'S' in line or 'G' in line:
#        print(line, "Line number:", fileinput.lineno())
#fileinput.close()

