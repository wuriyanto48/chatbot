import tensorflow as tf
import numpy as np
import os
import re
import nltk
import string
import textdistance
import pickle
import pandas as pd

from .dnn import create_model, create_model_from_dnn

from nltk.stem.lancaster import LancasterStemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, '../model/h5/model.h5')
TF_MODEL_DIR = os.path.join(BASE_DIR, '../model/tf/tf')

DATA_DIR = os.path.join(BASE_DIR, '../data')

DATASET_BASE_WORD_BAHASA = os.path.join(DATA_DIR, 'base_word_bahasa.txt')
VOCAB_PICKLE_DIR = os.path.join(DATA_DIR, 'vocab.pickle')

'''
load base words bahasa from textfile
'''
def load_base_words_bahasa():
    base_words = []
    with open(DATASET_BASE_WORD_BAHASA, 'r') as file:
        base_words = [w.strip() for w in file.readlines()]
    return base_words

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

