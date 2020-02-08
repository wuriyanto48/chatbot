#!/usr/bin/env python

from model import test_classify, stem_text
import pandas as pd
import numpy as np

if __name__ == '__main__':
    df = pd.DataFrame(dtype=float, columns=['word', 'score'])
    df['word'] = ['hay', 'hoy', 'woy']
    df['score'] = [0.75, 0.66, 0.80]

    h = np.argmax(df['score'].values)
    print(df['word'][h])
    