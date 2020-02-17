#!/usr/bin/env python

import json
from core.trainer import Trainer
from core.datastore.dataset import Dataset
from config import DATASET_FILE

if __name__ == '__main__':

    dataset = {}

    with open(DATASET_FILE) as file:
        dataset = json.load(file)

    # host = 'localhost'
    # port = 27017
    # username = 'bot'
    # password = 'bot'
    # database = 'bot_dataset'

    # datastore = Dataset(host=host, port=port, username=username, password=password, database=database)

    # dataset = datastore.find_all()

    trainer = Trainer(dataset['collections'])
    # trainer = Trainer(dataset=dataset)
    trainer.train()