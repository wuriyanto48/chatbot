from flask import Flask, request, jsonify

import json
import random as rd
import pandas as pd
import numpy as np
from model import load_model, do_answer, get_bag_of_words, DATASET_FILE

app = Flask(__name__)

@app.route('/')
def index():
	return 'welcome'

@app.errorhandler(400)
def page_empty_payload(error):
	response = jsonify({'message': 'payload cannot be empty'})
	return response, 400

@app.errorhandler(404)
def page_not_found(error):
	response = jsonify({'message': 'page not found'})
	return response, 404

@app.errorhandler(500)
def page_not_found(error):
	response = jsonify({'message': 'server under maintenance'})
	return response, 500

@app.route('/bot', methods=['POST'])
def chat():
    payload = request.json
    sentence = payload['sentence']
    if (sentence == ''):
        response = jsonify({'message': 'sentence cannot be empty'})
        return response

    reply = do_answer(sentence)

    response = jsonify({'reply': reply})
    return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)