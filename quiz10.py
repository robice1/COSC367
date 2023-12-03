import math

def euclidean_distance(v1, v2):
    squared_dist = sum((x - y) ** 2 for x, y in zip(v1, v2))
    distance = math.sqrt(squared_dist)
    return distance

from collections import Counter

def majority_element(labels):
    label_counts = Counter(labels)
    most_common_labels = label_counts.most_common()
    print(most_common_labels)
    majority_label = most_common_labels[0][0]
    return majority_label

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

def construct_perceptron(weights, bias):
    """Returns a perceptron function using the given paramers."""
    def perceptron(input):
        weighted_sum = sum(w * x for w, x in zip(weights, input)) + bias
        return 1 if weighted_sum >= 0 else 0
    
    return perceptron

def accuracy(classifier, inputs, expected_outputs):
    correct_predictions = 0
    for input, expected_output in zip(inputs, expected_outputs):
        prediction = classifier(input)
        if prediction == expected_output:
            correct_predictions += 1
    accuracy = correct_predictions / len(inputs)
    return accuracy

def learn_perceptron_parameters(weights, bias, training_examples, learning_rate, max_epochs):
    for _ in range(max_epochs):
        for input, expected_output in training_examples:
            prediction = construct_perceptron(weights, bias)(input)
            for i in range(len(weights)):
                weights[i] += input[i] * learning_rate * (expected_output - prediction)
            bias += learning_rate * (expected_output - prediction)
    return (weights, bias)

weights = [2, -4]
bias = 0
learning_rate = 0.5
examples = [
  ((0, 0), 0),
  ((0, 1), 0),
  ((1, 0), 0),
  ((1, 1), 1),
  ]
max_epochs = 50

weights, bias = learn_perceptron_parameters(weights, bias, examples, learning_rate, max_epochs)
print(f"Weights: {weights}")
print(f"Bias: {bias}\n")

perceptron = construct_perceptron(weights, bias)

print(perceptron((0,0)))
print(perceptron((0,1)))
print(perceptron((1,0)))
print(perceptron((1,1)))
print(perceptron((2,2)))
print(perceptron((-3,-3)))
print(perceptron((3,-1)))