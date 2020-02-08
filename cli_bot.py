#!/usr/bin/env python

import json
import random as rd
import pandas as pd
import numpy as np
from model import load_model, do_answer, get_bag_of_words, DATASET_FILE

'''
answer will answer to every given question 
'''
def answer():
    model, (words, labels, training, output) = load_model()

    print("type (q) to stop!")
    while True:
        sentence = input("You: ")
        if sentence.lower() == "q":
            break

        answ = do_answer(sentence)
        print(answ)

def cli():
    answer()

if __name__ == '__main__':
    cli()