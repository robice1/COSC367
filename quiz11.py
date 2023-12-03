def max_value(tree):
    if isinstance(tree, list):
        value = float("-inf")
        for child in tree:
            value = max(value, min_value(child))
        return value
    else:
        return tree
    
def min_value(tree):
    if isinstance(tree, list):
        value = float("inf")
        for child in tree:
            value = min(value, max_value(child))
        return value
    else:
        return tree


def max_action_value(game_tree):
    if not isinstance(game_tree, list):
        return (None, game_tree)
    best_action = None
    best_value = float("-inf")
    for action, child in enumerate(game_tree):
        _, value = min_action_value(child)
        if value > best_value or (value == best_value and (best_action is None or action < best_action)):
            best_value = value
            best_action = action
    return (best_action, best_value)

def min_action_value(game_tree):
    if not isinstance(game_tree, list):
        return (None, game_tree)
    best_action = None
    best_value = float("inf")
    for action, child in enumerate(game_tree):
        _, value = max_action_value(child)
        if value < best_value or (value == best_value and (best_action is None or action < best_action)):
            best_value = value
            best_action = action
    return (best_action, best_value)

from math import inf

def prune_tree(game_tree, alpha=-inf, beta=inf):
    if not isinstance(game_tree, list):
        # If the tree is a leaf node, return the node's value and update alpha and beta.
        return game_tree, alpha, beta

    pruned_tree = []
    pruning_events = []

    for child in game_tree:
        child_pruned, new_alpha, new_beta = prune_tree(child, alpha, beta)
        pruned_tree.append(child_pruned)

        if alpha >= beta:
            # Pruning event occurred, add the (alpha, beta) pair to pruning_events.
            pruning_events.append((alpha, beta))
            break

        if alpha < new_alpha:
            alpha = new_alpha
        if beta > new_beta:
            beta = new_beta

    return pruned_tree, alpha, beta

# Given explicit game tree
game_tree = [2, [-1, 5], [1, 3], 4]

# Prune the tree with alpha-beta pruning
pruned_tree, alpha, beta = prune_tree(game_tree)

print("Pruned Tree:", pruned_tree)
