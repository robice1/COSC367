from search import *
from math import sqrt

class LocationGraph(Graph):
    def __init__(self, location, radius, starting_nodes, goal_nodes):
        self.location = location
        self.radius = radius
        self._starting_nodes = starting_nodes
        self.goal_nodes = goal_nodes
    
    def starting_nodes(self):
        return self._starting_nodes
    
    def is_goal(self, node):
        return node in self.goal_nodes
    
    def outgoing_arcs(self, tail):
        arcs = []
        for head, head_location in self.location.items():
            if head != tail:
                tail_location = self.location[tail]
                distance = sqrt((head_location[0] - tail_location[0])**2 + (head_location[1] - tail_location[1])**2)
                if distance <= self.radius:
                    action = f"{tail}->{head}"
                    arc = Arc(tail, head, action, distance)
                    arcs.append(arc)
        return sorted(arcs, key=lambda x: x.head)

import heapq
from search import Frontier

sequence_number = 0

class LCFSFrontier(Frontier):
    def __init__(self):
        self._priority_queue = []
        heapq.heapify(self._priority_queue)
    
    def add(self, path):
        global sequence_number
        cost = sum(arc.cost for arc in path)
        heapq.heappush(self._priority_queue, (cost, sequence_number, path))
        sequence_number += 1
    
    def __next__(self):
        if not self._priority_queue:
            raise StopIteration
        _, _, path = heapq.heappop(self._priority_queue)
        return path
    

graph = LocationGraph(
    location={'A': (25, 7),
              'B': (1, 7),
              'C': (13, 2),
              'D': (37, 2)},
    radius=15,
    starting_nodes=['B'],
    goal_nodes={'D'}
)

solution = next(generic_search(graph, LCFSFrontier()))
print_actions(solution)