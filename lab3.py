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
    clauses_list = list(clauses(knowledge_base))
    while True:
        selected = None
        for h, b in clauses_list:
            if all(atom in C for atom in b) and h not in C:
                selected = h
                break
        if selected is None:
            break
        C.add(selected)
    return C

from search import *

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
                outgoing = [b if x == h else x for x in tail_node]
                
                arcs.append(Arc(tail_node, list(itertools.chain.from_iterable(outgoing)), str(tail_node) + '->' + str(list(itertools.chain.from_iterable(outgoing))), 1))
        return arcs
        

class DFSFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty stack."""
        self.container = []

    def add(self, path):
        """Adds a new path to the frontier. A path is a sequence (tuple) of
        Arc objects."""
        self.container.append(path)

    def __iter__(self):
        """The object returns itself because it is implementing a __next__
        method and does not need any additional state for iteration."""
        return self
        
    def __next__(self):
        """Selects, removes, and returns a path on the frontier if there is
        any.Recall that a path is a sequence (tuple) of Arc
        objects. Override this method to achieve a desired search
        strategy. If there nothing to return this should raise a
        StopIteration exception.
        """        
        if len(self.container) > 0:
            current_path = self.container.pop()
            return current_path
        else:
            raise StopIteration   # don't change this one

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