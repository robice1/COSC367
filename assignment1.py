from search import *
import math
from heapq import heappush, heappop

class RoutingGraph(Graph):
    def __init__(self, map_str):
        self.map_str = map_str
        self.map_lst = []
        for ln in map_str.strip().split('\n'):
            self.map_lst.append(ln.strip())
        self.rows = len(self.map_lst)
        self.cols = len(self.map_lst[0])
        self.portals = []
        self.fuel_stations = []
        self.agents = []
        self.goals = []
        for row in range(self.rows):
            for col in range(self.cols):
                char = self.map_lst[row][col]
                if char == 'P':
                    self.portals.append((row, col))
                elif char == 'F':
                    self.fuel_stations.append((row, col))
                elif char == 'S':
                    self.agents.append((row, col, math.inf))
                elif char.isdigit():
                    self.agents.append((row, col, int(char)))
                elif char == 'G':
                    self.goals.append((row, col))
    
    def is_goal(self, node):
        row, col, fuel = node
        if (row, col) in self.goals:
            return True
        return False
    
    def starting_nodes(self):
        return self.agents
    
    def outgoing_arcs(self, tail_node):
        row, col, fuel = tail_node
        arcs = []
        moves = [('N' , -1, 0),
                 ('E' ,  0, 1),
                 ('S' ,  1, 0),
                 ('W' ,  0, -1),]
        for move, v, h in moves:
            new_row, new_col, new_fuel = row + v, col + h, fuel - 1
            if 0 < new_row < (self.rows - 1) and 0 < new_col < (self.cols - 1) and fuel > 0:
                dest_char = self.map_lst[new_row][new_col]
                if dest_char != 'X':
                    cost = 5
                    arcs.append(Arc(tail_node, (new_row, new_col, new_fuel), move, cost))
        if self.map_lst[row][col] == 'F' and fuel < 9:
            arcs.append(Arc(tail_node, (row, col, 9), 'Fuel up', 15))
        if self.map_lst[row][col] == 'P':
            for portal_row, portal_col in self.portals:
                if (portal_row, portal_col) != (row, col):
                    arcs.append(Arc(tail_node, (portal_row, portal_col, fuel), f'Teleport to ({portal_row}, {portal_col})', 10))
        return arcs
    
    def estimated_cost_to_goal(self, node):
        min_dist = math.inf
        for goal in self.goals:
            distance = abs(node[0] - goal[0]) + abs(node[1] - goal[1])
            min_dist = min(min_dist, distance)
        return min_dist * 5

class AStarFrontier(Frontier):
    def __init__(self, graph):
        self.graph = graph
        self.frontier = []
        self.counter = 0
        self.visited = set()
        self.frontier_states = set()

    
    def add(self, path):
        total_cost = sum(arc.cost for arc in path)
        estimated_cost = self.graph.estimated_cost_to_goal(path[-1].head)
        priority = total_cost + estimated_cost
        state = path[-1].head
        if state not in self.visited and state not in self.frontier_states:
            heappush(self.frontier, (priority, self.counter, path))
            self.frontier_states.add(state)
            self.counter += 1
    
    def __next__(self):
        while self.frontier:
            _, _, path = heappop(self.frontier)
            if path[-1].head not in self.visited:
                self.frontier_states.remove(path[-1].head)
                self.visited.add(path[-1].head)
                return path
        raise StopIteration

def print_map(map_graph, frontier, solution):
    expanded = set()
    solution_path = set()
    for path in frontier.visited:
        expanded.add(path[:2])
    if solution:
        for arc in solution:
            solution_path.add(arc.head[:2])
    map_chars = [list(row) for row in map_graph.map_lst]
    for row in range(map_graph.rows):
        for col in range(map_graph.cols):
            if map_chars[row][col] not in '+-|XSG0123456789':
                if (row, col) in solution_path:
                    map_chars[row][col] = '*'
                elif (row, col) in expanded:
                    map_chars[row][col] = '.'
    for row in map_chars:
        print("".join(row))
    

def main():  
    map_str = """\
    +---------+
    |         |
    |    G    |
    |         |
    +---------+
    """
    
    map_graph = RoutingGraph(map_str)
    frontier = AStarFrontier(map_graph)
    solution = next(generic_search(map_graph, frontier), None)
    print_map(map_graph, frontier, solution)
    

if __name__ == "__main__":
    main()