def is_valid_expression(object, function_symbols, leaf_symbols):
    """Takes an object and tests whether it is a valid expression according to the definition of expressions in this assignment"""
    if type(object) == int:
        return True
    elif type(object) == str:
        return object in leaf_symbols
    elif type(object) == list and len(object) == 3 and object[0] in function_symbols:
        return is_valid_expression(object[1], function_symbols, leaf_symbols) and is_valid_expression(object[2], function_symbols, leaf_symbols)
    else:
        return False

def depth(expression):
    if type(expression) == int or type(expression) == str:
        return 0
    elif type(expression) == list and len(expression) == 3:
        return 1 + max(depth(expression[1]), depth(expression[2]))
    else:
        return -1

def evaluate(expression, bindings):
    if type(expression) == int:
        return expression
    elif type(expression) == str:
        return bindings[expression]
    elif type(expression) == list and len(expression) == 3:
        function_symbol = expression[0]
        func = bindings[function_symbol]
        var1 = evaluate(expression[1], bindings)
        var2 = evaluate(expression[2], bindings)
        return func(var1, var2)

import random

def random_expression(function_symbols, leaves, max_depth):
    if max_depth == 0 or random.random() < 0.5:
        return random.choice(leaves)
    else:
        function_symbol = random.choice(function_symbols)
        left_subtree = random_expression(function_symbols, leaves, max_depth - 1)
        right_subtree = random_expression(function_symbols, leaves, max_depth - 1)
        return [function_symbol, left_subtree, right_subtree]

def generate_rest(initial_sequence, expression, length):
    if length == 0:
        return []
    bindings = {'x':initial_sequence[-2], 'y':initial_sequence[-1], '+':lambda x, y: x+y,
                '-':lambda x, y : x-y,'*':lambda x ,y : x * y}
    result = initial_sequence[:]
    for i in range(len(initial_sequence), length + len(initial_sequence)):
        bindings['i'] = i
        new_value = evaluate(expression, bindings)
        result.append(new_value)
        bindings['x'] = result[-2]
        bindings['y'] = result[-1]
    return result[-length:]

def predict_rest(sequence):
    function_symbols = ['+', '-', '*']
    leaves = [-2, -1, 0, 1, 2, 'x', 'y', 'i']
    n = len(sequence)
    initial_sequence = sequence[:]
    while True:
        expression = random_expression(function_symbols, leaves, 3)
        check = generate_rest(initial_sequence[:2], expression, n - 2)
        if check == initial_sequence[2:]:
            predicted = generate_rest(initial_sequence, expression, 5)
            return predicted



bitmap = [99, 20, 8, 20, 99]
for bit in bitmap:
    print(format(bit, '08b'))
