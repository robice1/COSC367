from itertools import combinations

def n_queens_neighbours(state):
    return sorted([tuple(state[:i] + (state[j],) + state[i+1:j] + (state[i],) + state[j+1:]) for i, j in combinations(range(len(state)), 2)])

def n_queens_cost(state):
    n = len(state)
    return sum(1 for i, j in combinations(range(n), 2) if abs(state[i]-state[j]) == abs(i - j) or state[i]==state[j])


def greedy_descent(initial_state, neighbours, cost):
    current_state = initial_state
    trace = [current_state]
    while True:
        neighbour_states = neighbours(current_state)
        if not neighbour_states:
            break
        neighbour_costs = [cost(neighbour) for neighbour in neighbour_states]
        min_cost = min(neighbour_costs)
        if min_cost >= cost(current_state):
            break
        current_state = neighbour_states[neighbour_costs.index(min_cost)]
        trace.append(current_state)
    return trace

def greedy_descent_with_random_restart(random_state, neighbours, cost):
    restarts = 0
    while True:
        initial_state = random_state()
        print(initial_state)
        trace = greedy_descent(initial_state, neighbours, cost)
        for state in trace:
            if state != initial_state:
                print(state)
        if cost(trace[-1]) == 0:
            break
        restarts += 1
        print("RESTART")        

def roulette_wheel_select(population, fitness, r):
    total_fitness = sum(fitness(individual) for individual in population)
    threshold = r * total_fitness
    sum_fitness = 0.0
    for individual in population:
        individual_fitness = fitness(individual)
        sum_fitness += individual_fitness
        if sum_fitness >= threshold:
            return individual

population = [0, 1, 2]

def fitness(x):
    return x

for r in [0.001, 0.33, 0.34, 0.5, 0.75, 0.99]:
    print(roulette_wheel_select(population, fitness, r))