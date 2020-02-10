#!/usr/bin/env python

import json
from core.trainer import train
from config import DATASET_FILE

if __name__ == '__main__':

    dataset = {}

    with open(DATASET_FILE) as file:
        dataset = json.load(file)

    train(dataset=dataset['collections'])