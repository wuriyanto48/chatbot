import tensorflow as tf
import numpy as np
import os
import re
import random as rd
import json
import nltk
import string
import textdistance
import pickle
import pandas as pd

from dnn import create_model, create_model_from_dnn

from nltk.stem.lancaster import LancasterStemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, 'model/h5/model.h5')
TF_MODEL_DIR = os.path.join(BASE_DIR, 'model/tf/tf')
VOCAB_PICKLE_DIR = os.path.join(BASE_DIR, 'data/vocab.pickle')

DATA_DIR = os.path.join(BASE_DIR, 'data')
DATASET_FILE = os.path.join(DATA_DIR, 'dataset.json')

BATCH_SIZE = 5
EPOCHS = 1000

WORD_SIZE = 38
OUTPUT_SIZE = 6

'''
save tensorflow trained model
'''
def save_model(model, tokenizer):
    model.save(MODEL_DIR)

    with open(VOCAB_PICKLE_DIR, 'wb') as tp:
        pickle.dump(tokenizer, tp, protocol=pickle.HIGHEST_PROTOCOL)
    
'''
load tensorflow trained model from disk
'''
def load_model():
    with open(VOCAB_PICKLE_DIR, 'rb') as tp:
        tokenizer_data = pickle.load(tp)
    return (tf.keras.models.load_model(MODEL_DIR), tokenizer_data)

'''
load tf tensorflow trained model from disk
'''
def load_tf():
    with open(VOCAB_PICKLE_DIR, 'rb') as tp:
        tokenizer_data = pickle.load(tp)
    (words, labels, training_data, output) = tokenizer_data
    model = create_model_from_dnn(len(words), len(output[0]), TF_MODEL_DIR, VOCAB_PICKLE_DIR)
    model.load_weights(TF_MODEL_DIR)
    return (model, tokenizer_data)

'''
clear stop words will remove all meaningless words
'''
def clear_stop_words(sentence):
    list_stop_word_ID = set(nltk.corpus.stopwords.words('indonesian'))
    tokens = nltk.word_tokenize(sentence)
    
    return [t for t in tokens if t not in list_stop_word_ID]

'''
clean text will remove stemmed text from sentence
'''
def stem_text(text):
    # stemmer is to find the root of the word
    # eg: loved = love, loves = love, singing = sing
    # for english word
    #stemmer = LancasterStemmer()

    # for indonesian word
    stemmerFactory = StemmerFactory()
    stemmer = stemmerFactory.create_stemmer()

    if type(text) is str:
        words = nltk.word_tokenize(text)
        return [stemmer.stem(word.lower()) for word in words]

    return [stemmer.stem(word.lower()) for word in text]

'''
get bag of words will convert sentence to bag of words using words list
'''
def get_bag_of_words(sentence, words, verbose=True):

    THRESHOLD = 0.65

    # create array of 0 with lenght of words
    bag = [0 for _ in range(len(words))]

    sentence_words = stem_text(sentence)

    df = pd.DataFrame(dtype=float, columns=['word', 'score'])
    pred_word = []
    scores = []
    for sw in sentence_words:
        for i, w in enumerate(words):
            r = textdistance.hamming.normalized_similarity(sw, w)
            if r >= THRESHOLD:
                bag[i] = 1
                pred_word.append(w)
                scores.append(r)

                if verbose:
                    print('bag found : {}, similarity: {}'.format(w, r))
    df['word'] = pred_word
    df['score'] = scores

    print(df)

    highest_scored_word_index = np.argmax(df['score'].values)
    return (np.array(bag), df['word'][highest_scored_word_index], df['score'][highest_scored_word_index])

'''
test model
'''
def test_model(sentence):
    model, (words, labels, training_data, output) = load_model()
    (bags, pred_word, r) = get_bag_of_words(sentence, words)
    print(bags)
    print(words)

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
    print('--input--')
    print(input_data.values)
    
    predicted = model.predict(input_data.values)[0]
    results_index = np.argmax(predicted)
    print(predicted)
    tag = labels[results_index]

    print(tag)
    
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

    for data in dataset["collections"]:
        if data['tag'] == tag:
            responses = data['responses']
    

    answer = ''
    if r > 0.80:
        choice = rd.choice(responses)
        answer = choice
    else:
        choice = rd.choice(responses)
        answer = 'Apakah maksud anda "{}"?, {}'.format(pred_word, choice)
    return answer

def preprocess_dataset():

    words = []
    labels = []
    docs_x = []
    docs_y = []

    dataset = {}

    with open(DATASET_FILE) as file:
        dataset = json.load(file)

    for intent in dataset['collections']:
        for pattern in intent['patterns']:

            # case folding
            pattern = re.sub(r"\d+", "", pattern)
            pattern = pattern.translate(str.maketrans("","", string.punctuation)).strip()

            # tokenize word
            word_token = nltk.word_tokenize(pattern)
            # insert word token to database vacabulary
            words.extend(word_token)

            docs_x.append(word_token)
            docs_y.append(intent['tag'])

        if intent['tag'] not in labels:
            # create unique label/ class
            labels.append(intent['tag'])

    # words stemming of list pattern
    words = stem_text(words)

    # create list of unique stemmed words
    words = sorted(list(set(words)))
    labels = sorted(labels)

    return (words, labels, docs_x, docs_y)

'''
train model
'''
def train():
    
    (words, labels, docs_x, docs_y) = preprocess_dataset()

    # bag of words
    training_data = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        word_stemmed = stem_text(doc)
        
        for w in words:
            if w in word_stemmed:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training_data.append(bag)
        output.append(output_row)

    # convert to numpy array
    training_data = np.array(training_data)
    output = np.array(output)

    model = create_model(len(words), len(output[0]))
    # model = create_model_from_dnn(len(words), len(output[0]), TF_MODEL_DIR, VOCAB_PICKLE_DIR)
    model.fit(training_data, output, batch_size=BATCH_SIZE , epochs=EPOCHS)
    
    save_model(model, (words, labels, training_data, output))
    # model.save((words, labels, training_data, output))
