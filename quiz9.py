import csv
def posterior(prior, likelihood, observation):
    num = 1
    den = 1
    for i in range(0, len(observation)):
        if observation[i]:
            num *= likelihood[i][observation[i]]
            den *= likelihood[i][not observation[i]]
        else:
            num *= (1 - likelihood[i][not observation[i]])
            den *= (1 - likelihood[i][observation[i]])
    val = (prior * num) + ((1 - prior) * den)
    post_prob = (prior * num) / val
    return post_prob

def learn_prior(file_name, pseudo_count=0):
    spam_count = pseudo_count
    non_spam_count = pseudo_count
    with open(file_name) as in_file:
        reader = csv.reader(in_file)
        next(reader)
        for row in reader:
            label = int(row[-1])
            if label == 1:
                spam_count += 1
            else:
                non_spam_count += 1
    total_count = spam_count + non_spam_count
    prior = spam_count / total_count
    return prior

import csv
import os
import pandas as pd

def learn_likelihood(file_name, pseudo_count=0):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(script_dir, 'spam-labelled.csv')
    df = pd.read_csv(file_name)
    spam_count = (df['SPAM'] == 1).sum()
    non_spam_count = (df['SPAM'] == 0).sum()
    true_counts = [0 for _ in range(df.shape[1]-1)]
    false_counts = [0 for _ in range(df.shape[1]-1)]
    likelihoods = [[0,0] for x in range(df.shape[1]-1)]
    for index, obs in df.iterrows():
        for i in range(0, len(obs) - 1):
            if obs[i] == 1 and obs[len(obs)-1] == 0:
                false_counts[i] += 1
            elif obs[i] == 1 and obs[len(obs)-1] == 1:
                true_counts[i] += 1
    for i in range(0, len(true_counts)):
        likelihoods[i][True] = (true_counts[i] + pseudo_count) / (spam_count + pseudo_count * 2)
        likelihoods[i][False] = (false_counts[i] + pseudo_count) / (non_spam_count + pseudo_count * 2)
    return likelihoods


def nb_classify(prior, likelihood, input_vector):
    val = posterior(prior, likelihood, input_vector)
    if val > 0.5:
        return ("Spam", val)
    else:
        return ("Not Spam", 1 - val)


prior = learn_prior("C:/users/robbi/COSC367/spam-labelled.csv")
likelihood = learn_likelihood("C:/users/robbi/COSC367/spam-labelled.csv")

input_vectors = [
    (1,1,0,0,1,1,0,0,0,0,0,0),
    (0,0,1,1,0,0,1,1,1,0,0,1),
    (1,1,1,1,1,0,1,0,0,0,1,1),
    (1,1,1,1,1,0,1,0,0,1,0,1),
    (0,1,0,0,0,0,1,0,1,0,0,0),
    ]

predictions = [nb_classify(prior, likelihood, vector) 
               for vector in input_vectors]

for label, certainty in predictions:
    print("Prediction: {}, Certainty: {:.5f}"
          .format(label, certainty))