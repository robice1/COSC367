from search import *
from collections import deque

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
        return [Arc(tail_node, tail_node - 1, action="1down", cost=1),
                Arc(tail_node, tail_node + 2, action="2up", cost=1)]
    
    def starting_nodes(self):
        return [self.starting_number]
    
    def is_goal(self, node):
        return node % 10 == 0

from search import *
import copy

BLANK = ' '

class SlidingPuzzleGraph(Graph):
    """Objects of this type represent (n squared minus one)-puzzles.
    """

    def __init__(self, starting_state):
        self.starting_state = starting_state

    def outgoing_arcs(self, state):
        """Given a puzzle state (node) returns a list of arcs. Each arc
        represents a possible action (move) and the resulting state."""
        
        n = len(state) # the size of the puzzle
        
        # Find i and j such that state[i][j] == BLANK
        for row in range(n):
            for col in range(n):
                if state[row][col] == BLANK:
                    i, j = row, col
        
        arcs = []
        if i > 0:
            action = "Move {} down".format(state[i-1][j]) # or blank goes up
            new_state = copy.deepcopy(state) 
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], BLANK
            arcs.append(Arc(state, new_state, action, 1))
        if i < n - 1:
            action = "Move {} up".format(state[i+1][j]) # or blank goes down
            new_state = copy.deepcopy(state) 
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], BLANK
            arcs.append(Arc(state, new_state, action, 1))
        if j > 0:
            action = "Move {} right".format(state[i][j-1]) # or blank goes left
            new_state = copy.deepcopy(state) 
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], BLANK
            arcs.append(Arc(state, new_state, action, 1))
        if j < n - 1:
            action = "Move {} left".format(state[i][j+1])
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], BLANK
            arcs.append(Arc(state, new_state, action, 1))
        return arcs

    def starting_nodes(self):
        return [self.starting_state]
    
    def is_goal(self, state):
        """Returns true if the given state is the goal state, False
        otherwise. There is only one goal state in this problem."""
        
        n = len(state)
        if state[0][0] != BLANK:
            return False
        checker = 0
        for i in range(n):
            for j in range(n):
                if state[i][j] == BLANK:
                    checker += 1
                else:
                    if checker != state[i][j]:
                        return False
                    checker += 1
        return True
        

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
                distance = sqrt((head_location[0] - tail_location[0])**2 + (head_location[1] - tail_location[1])**2)
                if distance <= self.radius:
                    action = f"{tail}->{head}"
                    arc = Arc(tail, head, action, distance)
                    arcs.append(arc)
        return sorted(arcs, key=lambda x: x.head)

import heapq
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
        if len(self._priority_queue) > 0:
            _, _, path = heapq.heappop(self._priority_queue)
            return path
        else:
            raise StopIteration

import itertools

def interpretations(atoms):
    atoms = sorted(atoms)
    n = len(atoms)
    combinations = itertools.product([False, True], repeat=n)
    interps = []
    for combination in combinations:
        interp = {}
        for i in range(n):
            interp[atoms[i]] = combination[i]
        interps.append(interp)
    return interps

def atoms(formula):
    """Takes a formula in the form of a lambda expression and returns a set of
    atoms used in the formula. The atoms are parameter names represented as
    strings.
    """
    
    return {atom for atom in formula.__code__.co_varnames}
    
def value(formula, interpretation):
    """Takes a formula in the form of a lambda expression and an interpretation
    in the form of a dictionary, and evaluates the formula with the given
    interpretation and returns the result. The interpretation may contain
    more atoms than needed for the single formula.
    """
    arguments = {atom: interpretation[atom] for atom in atoms(formula)}
    return formula(**arguments)


def models(knowledge_base):
    all_atoms = set()
    for formula in knowledge_base:
        all_atoms = atoms(formula) | all_atoms
    interps = interpretations(all_atoms)
    model_interps = []
    for interp in interps:
        if all(value(formula, interp) for formula in knowledge_base):
            model_interps.append(interp)
    return model_interps

import re

def clauses(knowledge_base):
    """Takes the string of a knowledge base; returns an iterator for pairs
    of (head, body) for propositional definite clauses in the
    knowledge base. Atoms are returned as strings. The head is an atom
    and the body is a (possibly empty) list of atoms.

    -- Kourosh Neshatian - 2 Aug 2021

    """
    ATOM   = r"[a-z][a-zA-Z\d_]*"
    HEAD   = rf"\s*(?P<HEAD>{ATOM})\s*"
    BODY   = rf"\s*(?P<BODY>{ATOM}\s*(,\s*{ATOM}\s*)*)\s*"
    CLAUSE = rf"{HEAD}(:-{BODY})?\."
    KB     = rf"^({CLAUSE})*\s*$"

    assert re.match(KB, knowledge_base)

    for mo in re.finditer(CLAUSE, knowledge_base):
        yield mo.group('HEAD'), re.findall(ATOM, mo.group('BODY') or "")

def forward_deduce(knowledge_base):
    C = set()
    all_clause = list(clauses(knowledge_base))
    while True:
        selected = None
        for h, b in all_clause:
            if all(atom in C for atom in b) and h not in C:
                selected = h
                break
        if not selected:
            break
        C.add(selected)
    return C

class KBGraph(Graph):
    def __init__(self, kb, query):
        self.clauses = list(clauses(kb))
        self.query = query

    def starting_nodes(self):
        return [*self.query,]
        
    def is_goal(self, node):
        return len(node) == 0

    def outgoing_arcs(self, tail_node):
        arcs = []
        for h, b in self.clauses:
            if h in tail_node:
                outgoing = [b if x==h else x for x in tail_node]
                arcs.append(Arc(tail_node, list(itertools.chain.from_iterable(outgoing)), str(tail_node) + '->' + str(list(itertools.chain.from_iterable(outgoing))), 1))
        return arcs

class DFSFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""
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

def main():
    kb = """
    a :- b, c.
    b :- d, e.
    b :- g, e.
    c :- e.
    d.
    e.
    f :- a,
        g.
    """

    query = {'a'}
    if next(generic_search(KBGraph(kb, query), DFSFrontier()), None):
        print("The query is true.")
    else:
        print("The query is not provable.")



if __name__ == "__main__":
    main()