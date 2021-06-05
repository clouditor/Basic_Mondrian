# !/usr/bin/env python
# coding=utf-8

# this class exposes the necessary methods for the statistics service in the patient-community-example
from basic_mondrian_health.anonymizer import anonymize_health_data
from basic_mondrian_health.utils.generate_health_data import generate_one_record
from pymongo import MongoClient
import csv
import importlib

client = MongoClient("mongodb://localhost:27017/")
db = client.patient_data
collection = db.records

def anonymize_mongo_data(data):
    # save in health.data
    with importlib.resources.path('basic_mondrian_health.data', 'health.data') as path:
        with open(path, 'w') as out:
        # with open('data/health.data', 'w') as out:
            fields = ['group', 'timestamp', 'medication', 'medication_dosage', 'symptom', 'symptom_strength']
            write = csv.DictWriter(out, fieldnames=fields)
            for record in data: 
                write.writerow(record)

    # anonymize
    res = anonymize_health_data()

    # return anonymized data
    with importlib.resources.path('basic_mondrian_health.data', 'anonymized.data') as path:
        with open(path, newline='') as anonymized_file:
            data_array = []
            anonymized_file_reader = csv.reader(anonymized_file)
            for row in anonymized_file_reader:
                data_array.append(','.join(row))
            return data_array

def generate_record():
    return generate_one_record()

if __name__ == '__main__':
    # print(generate_record())
    
    # example data
    data = [
        {"group": "dementia", "timestamp": "2021-06-03T13:18:56+00:00", "medication": "hormonal", "medication_dosage": "3", "symptom": "tired", "symptom_strength": "5"},
        {"group": "dementia", "timestamp": "2021-06-03T13:18:56+00:01", "medication": "hormonal", "medication_dosage": "5", "symptom": "tired", "symptom_strength": "8"},
        {"group": "dementia", "timestamp": "2021-06-03T13:18:56+00:02", "medication": "hormonal", "medication_dosage": "9", "symptom": "tired", "symptom_strength": "7"}
    ]
    # alternatively, get data from the mongodb:
    # cursor = collection.find({}, {"_id": 0, "group": 1, "timestamp": 1, "medication": 1, "medication_dosage": 1, "symptom": 1, "symptom_strength": 1})
    # cursor = list(cursor)
    anonymize_mongo_data(data)