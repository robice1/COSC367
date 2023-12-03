from search import *

class DFSFrontier(Frontier):
    def __init__(self):
        self.container = []
    
    def add(self, path):
        self.container.append(path)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.container) > 0:
            return self.container.pop()
        else:
            raise StopIteration

from collections import deque

class BFSFrontier(Frontier):
    def __init__(self):
        self.container = deque([])
    
    def add(self, path):
        self.container.append(path)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.container) > 0:
            return self.container.popleft()
        else:
            raise StopIteration


class FunkyNumericGraph(Graph):
    def __init__(self, starting_number):
        self.starting_number = starting_number
    
    def outgoing_arcs(self, tail_node):
        return [Arc(tail_node, tail_node - 1, action='1down', cost=1),
                Arc(tail_node, tail_node + 2, action='2up', cost=1)]
    
    def starting_nodes(self):
        return [self.starting_number]
    
    def is_goal(self, node):
        return node % 10 == 0


from search import Arc, Graph
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
                distance = sqrt((head_location[0] - tail_location[0]) ** 2 + (head_location[1]-tail_location[1]) ** 2)
                if distance <= self.radius:
                    action = f"{tail}->{head}"
                    arc = Arc(tail, head, action, distance)
                    arcs.append(arc)
        return sorted(arcs, key=lambda x: x.head)
    
