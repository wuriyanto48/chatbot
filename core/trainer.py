import re
import nltk
import string
import textdistance
import numpy as np

from .dnn import create_model, create_model_from_dnn
from .model import stem_text, load_base_words_bahasa, save_model

BATCH_SIZE = 5
EPOCHS = 1000

THRESHOLD_SIMILARITY = 0.63

'''
Trainer class will train tensorflow model
'''
class Trainer(object):
    def __init__(self, dataset = []):
        self.dataset = dataset

        self.words = []
        self.labels = []
        self.docs_x = []
        self.docs_y = []
    
    def __preprocess(self):
        for intent in self.dataset:
            for pattern in intent['patterns']:

                # case folding
                pattern = re.sub(r"\d+", "", pattern)
                pattern = pattern.translate(str.maketrans("","", string.punctuation)).strip()

                # tokenize word
                word_token = nltk.word_tokenize(pattern)
                # insert word token to database vacabulary
                self.words.extend(word_token)

                self.docs_x.append(word_token)
                self.docs_y.append(intent['tag'])

            if intent['tag'] not in self.labels:
                # create unique label/ class
                self.labels.append(intent['tag'])

        # words stemming of list pattern
        self.words = stem_text(self.words)

        # base_word_bahasa = load_base_words_bahasa()
        # words.extend(base_word_bahasa)

        # create list of unique stemmed words
        self.words = sorted(list(set(self.words)))
        self.labels = sorted(self.labels)

    def train(self):

        self.__preprocess()

        # bag of words
        training_data = []
        output = []

        out_empty = [0 for _ in range(len(self.labels))]
        for x, doc in enumerate(self.docs_x):
            bag = [0 for _ in range(len(self.words))]

            word_stemmed = stem_text(doc)

            for ws in word_stemmed:
                for i, w in enumerate(self.words):
                    r = textdistance.hamming.normalized_similarity(ws, w)
                    if r >= THRESHOLD_SIMILARITY:
                        bag[i] = 1
            
            output_row = out_empty[:]
            output_row[self.labels.index(self.docs_y[x])] = 1

            training_data.append(bag)
            output.append(output_row)

        # convert to numpy array
        training_data = np.array(training_data)
        output = np.array(output)

        model = create_model(len(self.words), len(output[0]))
        # model = create_model_from_dnn(len(self.words), len(output[0]), TF_MODEL_DIR, VOCAB_PICKLE_DIR)
        model.fit(training_data, output, batch_size=BATCH_SIZE , epochs=EPOCHS)
        
        save_model(model, (self.words, self.labels, training_data, output))
        # model.save((self.words, self.labels, training_data, output))