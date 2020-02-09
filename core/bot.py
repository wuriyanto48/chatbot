import json
import textdistance
import pandas as pd
import numpy as np
import random as rd
from .model import stem_text, load_model, DATASET_FILE
from .trainer import THRESHOLD_SIMILARITY

'''
get bag of words will convert sentence to bag of words using words list
'''
def get_bag_of_words(sentence, words, verbose=True):

    # create array of 0 with lenght of words
    bag = [0 for _ in range(len(words))]

    sentence_words = stem_text(sentence)
    # sentence_words = clear_stop_words(sentence)

    df = pd.DataFrame(dtype=float, columns=['word', 'score'])
    pred_word = []
    scores = []
    for sw in sentence_words:
        for i, w in enumerate(words):
            r = textdistance.hamming.normalized_similarity(sw, w)
            if r >= THRESHOLD_SIMILARITY:
                bag[i] = 1
                pred_word.append(w)
                scores.append(r)

                if verbose:
                    print('bag found : {}, similarity: {}'.format(w, r))
    df['word'] = pred_word
    df['score'] = scores

    if not df.empty:
        highest_scored_word_index = np.argmax(df['score'].values)
        return (np.array(bag), df['word'][highest_scored_word_index], df['score'][highest_scored_word_index])

    return (np.array(bag), '', 0.0)


'''
test classify
'''
def test_classify(sentence):
    model, (words, labels, training_data, output) = load_model()
    print(type(model))
    THRESHOLD = 0.25
    # generate probabilities from the model

    (bags, pred_word, r) = get_bag_of_words(sentence, words)
    input_data = pd.DataFrame([bags], dtype=float, index=['input'])
    
    predicted = model.predict(input_data)[0]
    results_index = np.argmax(predicted)
    print(predicted)
    tag = labels[results_index]

    print(tag)
    print(training_data)
    
    # filter predicted data by threshold
    # predicted = [[i, p] for i, p in enumerate(predicted) if p > THRESHOLD]
    
    # predicted.sort(key=lambda x: x[1], reverse=True)

    # prob_list = []
    # for r in predicted:
    #     prob_list.append((labels[r[0]], str(r[1])))
    
    # print(prob_list)

'''
do_answer
'''
def do_answer(sentence):
    model, (words, labels, training_data, output) = load_model()

    (bags, pred_word, r) = get_bag_of_words(sentence, words)
    input_data = pd.DataFrame([bags], dtype=float, index=['input'])

    results = model.predict(input_data)[0]
    results_index = np.argmax(results)
    tag = labels[results_index]

    print(labels)
    print(tag)

    dataset = {}
    with open(DATASET_FILE) as file:
        dataset = json.load(file)

    responses = []
    for data in dataset["collections"]:
        if data['tag'] == tag:
            responses = data['responses']
    
    if r > 0.80:
        choice = rd.choice(responses)
        return choice

    if r == 0.0:
        choice = rd.choice(responses)
        return choice

    choice = rd.choice(responses)   
    answer = 'Apakah maksud anda "{}"?, {}'.format(pred_word, choice)
    return answer