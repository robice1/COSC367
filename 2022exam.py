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
    return sorted(C)

def knn_predict(input, examples, distance, combine, k):
    distances = [(example[0], distance(input, example[0]), example[1]) for example in examples]
    sorted_distances = sorted(distances, key=lambda x: (x[1], x[0]))
    k_distances = sorted_distances[:k]
    while True:
        if k == len(sorted_distances):
            break
        elif k_distances[-1][1] == sorted_distances[k][1]:
            k_distances.append(sorted_distances[k])
            k += 1
        else:
            break
    class_counts = []
    for point in k_distances:
        class_label = point[2]
        class_counts.append(class_label)
    prediction = combine(class_counts)
    return prediction

def num_crossovers(parent_expression1, parent_expression2):
    def count_nodes(expression):
        count = 0
        if isinstance(expression, list):
            for node in expression:
                if isinstance(node, list):
                    count += count_nodes(node)
                else:
                    count += 1
        else:
            return 1
        return count
    
    return count_nodes(parent_expression1) * count_nodes(parent_expression2)

def num_parameters(unit_counts):
    total_parameters = 0

    for i in range(1, len(unit_counts)):
        num_weights = unit_counts[i] * (unit_counts[i - 1] + 1)  # +1 for the bias term
        total_parameters += num_weights
    return total_parameters

print(num_parameters([2, 4, 2]))