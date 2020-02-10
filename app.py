#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

import json
import random as rd
import pandas as pd
import numpy as np
from core.bot import do_answer


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'app-client-1'
app.config['BASIC_AUTH_PASSWORD'] = 'app-pass-1'

basic_auth = BasicAuth(app)

@app.route('/')
def index():
	return 'welcome'

@app.errorhandler(400)
def page_empty_payload(error):
	response = jsonify({'message': 'payload cannot be empty'})
	return response, 400

@app.errorhandler(401)
def page_unauthorized(error):
	response = jsonify({'message': 'invalid authorization'})
	return response, 401

@app.errorhandler(404)
def page_not_found(error):
	response = jsonify({'message': 'page not found'})
	return response, 404

@app.errorhandler(500)
def page_not_found(error):
	response = jsonify({'message': 'server under maintenance'})
	return response, 500

@app.route('/bot', methods=['POST'])
@basic_auth.required
def chat():
    payload = request.json
    sentence = payload['sentence']
    if (sentence == ''):
        response = jsonify({'message': 'sentence cannot be empty'})
        return response, 400

    reply = do_answer(sentence)

    response = jsonify({'reply': reply})
    return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)