import graphics as g
import random

WIN_WIDTH = 800
WIN_HEIGHT = 800
LOCATION_CIRCLE_RADIUS = 5
UPDATE_RATE = 5

LINE_COLOR = g.color_rgb(200, 200, 200)
FRONTIER_COLOR = g.color_rgb(0, 0, 0)
NODE_COLOR = g.color_rgb(170, 0, 0)
SOLUTION_LINE_COLOR = "green"
SOLUTION_NODE_COLOR = "green"

GOAL_CITY = "Kuopio"
START_CITY = "Turku"

class Location:
    """
    name is the name of the city
    x, y are positions on a plane used when drawn. Maybe also in algorithms.
    connections is a list of other Location instances that describe where you can travel from self.
    """
    def __init__(self, name, x, y, connections):
        self.name = name;
        self.position = (x, y)
        self.connections = connections

    def draw(self, window, color=NODE_COLOR):
        position = {'x': self.position[0], 'y': self.position[1]}
        c = g.Circle(g.Point(position['x'], position['y']), LOCATION_CIRCLE_RADIUS)
        c.setFill(color)
        c.draw(window)
        label = g.Text(g.Point(position['x'], position['y'] - 20), self.name)
        label.draw(window)

def draw_main(window, locations):
    drawn_pairs = []
    for location in locations:
        locations[location].draw(window)
        for connection in locations[location].connections:
            # print(connection)
            # print(drawn_pairs)
            alreadyDrawn = False
            for pair in drawn_pairs:
                if pair[0] == location and pair[1] == connection.name:
                    alreadyDrawn = True
                if pair[1] == location and pair[0] == connection.name:
                    alreadyDrawn = True
            if not alreadyDrawn:
                l = g.Line(g.Point(locations[location].position[0], locations[location].position[1]),
                    g.Point(connection.position[0], connection.position[1]))
                l.setFill(LINE_COLOR)
                l.draw(window)
                drawn_pairs.append((location, connection.name))

def draw_solution(window, locations):
    for i in range(len(locations) - 1):
        locations[i].draw(window, SOLUTION_NODE_COLOR)
        x1, y1 = (locations[i].position[0], locations[i].position[1])
        x2, y2 = (locations[i + 1].position[0], locations[i + 1].position[1])
        line = g.Line(g.Point(x1, y1), g.Point(x2, y2))
        line.setFill(SOLUTION_LINE_COLOR)
        line.draw(window)

def drawFrontier(window, frontier_nodes):
    for i in frontier_nodes:
        i.state.draw(window, FRONTIER_COLOR)
        g.update(UPDATE_RATE)

def init_locations(town_map):
    # print("DEBUG!")
    locations = {}
    # Initialize locations without connections -->
    for key in town_map.keys():
        (x, y) = town_map[key]['position']
        locations[key] = Location(key, x, y, [])

    # Init connections with location instances
    for town in locations.keys():
        for connection in locations.keys():
            # If in the road map for town exist name of connection
            # Add connection location object to town connections
            # print(connection)
            if connection in town_map[town]['connections']:
                locations[town].connections.append(locations[connection])

    # for location in locations:
    #     print(locations[location].name)
    #     connection_str = ""
    #     for connection in locations[location].connections:
    #         connection_str += str(connection.name) + ", "
    #     print(connection_str)
    #     print("---------------")

    return locations

class Node:
    """
    state refers to a location object and parent to a node object.
    action refers to the action that generated the node.
    """
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state

    @property
    def path(self):
        if self.parent == None:
            return [self.state]
        else:
            return self.parent.path + [self.state]

# Action is a string that tells where we have travelled from parent
# e.g "Tampere" is parent so action could be "Helsinki"
def generate_node(parent, action):
    return Node(parent, action)

def goal_test(node, locations):
    # print(node.state.name)
    # print("GOAL: ")
    # print(locations[GOAL_CITY].name)
    # print(node.state.name == locations[GOAL_CITY].name)
    return node.state.name == locations[GOAL_CITY].name

def BFS(initial_state, generate_node, goal_test, locations, window=None):
    frontier = [Node(None, initial_state)]
    expanded_nodes = []

    try_counter = 0
    while len(frontier) > 0 and try_counter < 500:
        if window:
            drawFrontier(window, frontier)
        leaf = frontier.pop()
        if(goal_test(leaf, locations)):
            return leaf.path
        for connection in leaf.state.connections:
            new_node = Node(leaf, connection)
            if new_node.state.name in expanded_nodes:
                continue
            # if Node
            frontier = [Node(leaf, connection)] + frontier
        expanded_nodes.append(leaf.state.name)
    try_counter += 1
    return -1

def generate_random_town_map(location_amount, max_connections):
    town_map = {}
    # print(town_map.keys())
    # alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # alphabet += alphabet

    alphabet = [str(x) for x in range(location_amount)]

    for i in range(location_amount):
        print(str(i / location_amount * 100) + "% done!")
        label = random.choice(alphabet)
        while label in town_map.keys():
            label = random.choice(alphabet)
        # print(label)
        positionX = (random.randint(LOCATION_CIRCLE_RADIUS, WIN_WIDTH - LOCATION_CIRCLE_RADIUS))
        positionY = (random.randint(LOCATION_CIRCLE_RADIUS, WIN_HEIGHT - LOCATION_CIRCLE_RADIUS))
        town_map[label] = {'position': (positionX, positionY), 'connections': []}
    for local in town_map.keys():
        for i in range(random.randint(0, max_connections)):
            connection = random.choice(list(town_map.keys()))
            while connection == local:
                connection = random.choice(list(town_map.keys()))
            town_map[local]['connections'].append(connection)
    # print(town_map)

    return town_map
def main():
    # Initialize locations using TOWN_MAP
    TOWN_MAP = {
        'Turku': {
            'position': (100, 450),
            'connections': ['Helsinki', 'Tampere']
        },
        'Helsinki': {
            'position': (200, 500),
            'connections': ['Turku', 'Tampere', 'Mikkeli', 'Urjala']
        },
        'Tampere': {
            'position': (150, 250),
            'connections': ['Helsinki', 'Turku', 'Urjala']
        },
        'Jyvaskyla': {
            'position': (300, 100),
            'connections': ['Kuopio']
        },
        'Mikkeli': {
            'position': (400, 250),
            'connections': ['Kuopio', 'Helsinki']
        },
        'Kuopio': {
            'position': (450, 50),
            'connections': ['Mikkeli', 'Jyvaskyla']
        },
        'Urjala': {
            'position': (100, 300),
            'connections': ['Tampere', 'Helsinki']
        }
    };
    TOWN_MAP = generate_random_town_map(20, 5)
    global GOAL_CITY, START_CITY


    locations = init_locations(TOWN_MAP)
    win = g.GraphWin("BFS", WIN_WIDTH, WIN_HEIGHT, autoflush=True)
    draw_main(win, locations)
    START_CITY = str(input("Enter a start node: "))
    GOAL_CITY = str(input("Enter a goal node: ")) 

    solution = BFS(locations[START_CITY], generate_node, goal_test, locations)
    if solution == -1:
        print("NO SOLUTION!")
        return
    # print(solution)
    draw_solution(win, solution)
    solution_str = ""
    for node in solution:
        solution_str += " -> " + node.name
    print(solution_str)
    win.getMouse()
    draw_solution(win, solution)
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()
