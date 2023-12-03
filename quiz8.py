from itertools import product

def joint_prob(network, assignment):
    joint_probability = 1.0
    for variable_name, variable_value in assignment.items():
        cpt = network[variable_name]['CPT']
        if variable_name in network and 'Parents' in network[variable_name]:
            parents = network[variable_name]['Parents']
            parent_values = tuple(assignment[parent] for parent in parents)
        else:
            parent_values = ()
        prob = cpt.get(parent_values, 0.0)
        if not variable_value:
            prob = 1 - prob
        joint_probability *= prob
    return joint_probability


def query(network, query_var, evidence):
    
    # If you wish you can follow this template
    hidden_vars = network.keys() - evidence.keys() - {query_var}
    raw_distribution = [0.0,0.0]
    assignment = dict(evidence) # create a partial assignment
    for query_value in {True, False}:
        assignment[query_var] = query_value
        for values in product((True, False), repeat=len(hidden_vars)):
            hidden_assignments = {var:val for var,val in zip(hidden_vars, values)}
            assignment.update(hidden_assignments)
            joint_prob_assignment = joint_prob(network, assignment)
            if query_value:
                raw_distribution[1] += joint_prob_assignment
            else:
                raw_distribution[0] += joint_prob_assignment
    total_probability = sum(raw_distribution)
    normalized_distribution = [p / total_probability for p in raw_distribution]
    return tuple(normalized_distribution)    

network = {
    'A': {
        'Parents': [],
        'CPT': {
            (): 0.1
        }
    },
    'B': {
        'Parents': ['A'],
        'CPT': {
            (False,): 0.6,  # Probability of B=True given A=False
            (True,): 0.6,   # Probability of B=True given A=True
        }
    },
    'C': {
        'Parents': ['A'],
        'CPT': {
            (False,): 0.4,  # Probability of C=True given A=False
            (True,): 0.4,   # Probability of C=True given A=True
        }
    },
}


# We use the definition of independence here. B and C are
# independent if P(B,C) = P(B) * P(C). We sum over the joint
# to determine these values.

for b,c in product({True,False}, repeat=2):
    p_b_and_c = sum(joint_prob(network,{'A':a, 'B':b, 'C':c})
                    for a in {True, False})
    p_b = sum(joint_prob(network,{'A':a, 'B':b, 'C':c})
              for a, c in product({True, False}, repeat=2))
    p_c = sum(joint_prob(network,{'A':a, 'B':b, 'C':c})
              for a, b in product({True, False}, repeat=2))
    if abs(p_b_and_c - p_b * p_c) > 1e-10:
        print("It looks like B and C are still dependent.")
        break
else:
    print("OK")