#!/usr/bin/env python

from core.model import load_model
from core.bot import do_answer

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