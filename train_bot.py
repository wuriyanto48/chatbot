#!/usr/bin/env python

import json
from core.trainer import Trainer
from config import DATASET_FILE

if __name__ == '__main__':

    dataset = {}

    with open(DATASET_FILE) as file:
        dataset = json.load(file)

    trainer = Trainer(dataset['collections'])
    trainer.train()