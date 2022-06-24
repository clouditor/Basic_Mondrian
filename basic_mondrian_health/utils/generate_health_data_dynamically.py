# !/usr/bin/env python
# coding=utf-8
from flask import Flask, jsonify
import requests
import generate_health_data

app = Flask(__name__)

# - CONFIGURATION - #
BACKEND_URL = 'http://localhost:5000/'

# generates dynamically one realistic data record and sends it to the backend
@app.route('/post_one_new_realistic_data_record', methods=['POST'])
def post_health_data():
    record = generate_health_data.generate_one_realistic_record()
    response = requests.post(BACKEND_URL + 'post_health_data', data={'record_list': record})
    return response.status_code

# returns all stored data records on the backend
@app.route('/get_all_stored_data_records', methods=['GET'])
def get_health_data():
    response = requests.get(BACKEND_URL + 'get_health_data')
    return response.text # TODO: (lookup) evtl response.data

# generates a new realistic data set and returns it to requester
@app.route('/get_new_realistic_data_set', methods=['GET'])
def get_new_realistic_data_set():
    return jsonify({'data': generate_health_data.generate_realistic_data_set()})

# removes all stored data records on the backend
@app.route('/remove_all_stored_data_records', methods=['DELETE'])
def remove_health_data():
    response = requests.delete(BACKEND_URL + 'remove_health_data')
    return response.status_code





