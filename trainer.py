import re
import json
import nltk
import string
import textdistance
import numpy as np

from dnn import create_model, create_model_from_dnn
from model import DATASET_FILE, stem_text, load_base_words_bahasa, save_model

BATCH_SIZE = 5
EPOCHS = 1000

THRESHOLD_SIMILARITY = 0.63

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

    # base_word_bahasa = load_base_words_bahasa()
    # words.extend(base_word_bahasa)

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
        bag = [0 for _ in range(len(words))]

        word_stemmed = stem_text(doc)

        for ws in word_stemmed:
            for i, w in enumerate(words):
                r = textdistance.hamming.normalized_similarity(ws, w)
                if r >= THRESHOLD_SIMILARITY:
                    bag[i] = 1
        
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

    print(len(words))