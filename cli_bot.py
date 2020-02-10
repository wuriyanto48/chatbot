#!/usr/bin/env python

import json
from core.model import load_model
from core.bot import do_answer
from config import DATASET_FILE

'''
answer will answer to every given question 
'''
def answer(dataset = []):
    model, (words, labels, training, output) = load_model()

    print("type (q) to stop!")
    while True:
        sentence = input("You: ")
        if sentence.lower() == "q":
            break

        answ = do_answer(sentence, dataset=dataset)
        print(answ)

def cli():
    dataset = {}

    with open(DATASET_FILE) as file:
	    dataset = json.load(file)
    answer(dataset=dataset['collections'])

if __name__ == '__main__':
    cli()