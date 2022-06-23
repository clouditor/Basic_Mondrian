# !/usr/bin/env python
# coding=utf-8

import random
import os
import importlib

ATT_NAMES = ['group', 'timestamp', 'medication', 'medication_dosage', 'symptom', 'symptom_strength']
QI_INDEX = [0, 1, 2, 3, 4, 5]
IS_CAT = [True, True, True, False, True, False]
MAX_VALUE = [0, 0, 0, 1000, 0, 10]
VALUES = []

########################################################################################################################

# mapping of deseases to symptoms
disease_symptom_mapping = {
    'addiction': ['tired', 'weak', 'dry_mouth', 'sweaty', 'dizzy'],
    'adhd': ['tired', 'light-headed', 'sweaty', 'short_of_breath', 'sleep_normally'],
    'anxiety': ['tired', 'breathe_normally', 'remeber_normally', 'sleep_normally', 'sweaty'],
    'cancer': ['walk_normally', 'swallow_normally', 'sleep_normally', 'sweaty', 'tired', 'weak', 'dry_mouth', 'dizzy', 'short_of_breath', 'light-headed', 'breathe_normally', 'head', 'chest', 'extremities', 'chronic_pain'],
    'dementia': ['remember_normally', 'write_normally' 'walk_normally'],
    'depression': ['weak', 'tired', 'sleepy', 'dizzy', 'light-headed'],
    'mania': ['dry_mouth', 'thirsty', 'breathe_normally'],
    'neurological_disorder': ['head', 'walk_normally', 'move_one_side', 'weak', 'see_properly', 'light-headed'],
    'voice_disorder': ['sick', 'speak_normally', 'swallow_normally', 'breathe_normally'],
    'liver_disorder': ['skin', 'pass_urine_normally', 'abdomen', 'nausea']
}

# mapping of deseases to medications
disease_medication_mapping = {
    'addiction': ['hormonal', 'blood'],
    'adhd': ['hormonal', 'blood',],
    'anxiety': ['hormonal', 'blood',],
    'cancer': ['immunomodulating', 'hormonal', 'blood', 'dermatologic', 'gastrointestinal'],
    'dementia': ['hormonal', 'blood'],
    'depression': ['hormonal', 'blood'],
    'mania': ['hormonal', 'blood'],
    'neurological_disorder': ['hormonal', 'blood', 'immunomodulating'],
    'voice_disorder': ['respiratory'],
    'liver_disorder': ['blood']
}

def generate_one_realistic_record():
    parse_cat_values()
    record = ""
    disease_keys = list(disease_symptom_mapping.keys())
    disease_key = disease_keys[random.randint(0, len(disease_keys)-1)]
    record += disease_key + ","
    # pick one value of the defined timestamps
    path = 'data/health_' + ATT_NAMES[QI_INDEX[i]] + '.txt'
    data_file = open(path, 'r')
    values = []
    for line in data_file:
        line = line.strip()
        if len(line) == 0 or '?' in line:
            continue
        line = line.replace(' ', '')
        temp = line.split(';')
        values.append(temp[0])
    record += values[random.randint(0,len(values)-1)] + ","
    # choose medication depending on the disease
    medication_list = disease_medication_mapping[disease_key]
    record += medication_list[random.randint(0, len(medication_list)-1)] + ","
    # pick one random value of medication dosages
    record += str(random.randint(0, MAX_VALUE[3])) + ","
    # pick one random value of symptoms
    symptom_list = disease_symptom_mapping[disease_key]
    record += symptom_list[random.randint(0, len(symptom_list)-1)] + ","
    # pick one random value of symptom strengths
    record += str(random.randint(0, MAX_VALUE[5]))
    return record

def generate_realistic_data_set(size):
    data_set = []
    for i in range(size):
        data_set.append(generate_one_realistic_record())
    return data_set

def write_realistic_data_set_to_file(size):
    data_set = generate_realistic_data_set(size)
    if os.path.exists('data/health.data'):
        os.remove('data/health.data')
    with open('data/health.data', 'w') as f:
        for record in data_set:
            f.write(record + "\n")

########################################################################################################################

def generate_one_record():
    parse_cat_values()
    record = ""
    for i in range(len(QI_INDEX)):
        if IS_CAT[i] is False:
            record += str(random.randint(0, MAX_VALUE[i])) + ","
        else:
            with importlib.resources.path('basic_mondrian_health.data', 'health_' + ATT_NAMES[QI_INDEX[i]] + '.txt') as path:
                data_file = open(path, 'r')
                values = []
                for line in data_file:
                    line = line.strip()
                    if len(line) == 0 or '?' in line:
                        continue
                    line = line.replace(' ', '')
                    temp = line.split(';')
                    values.append(temp[0])
                record += values[random.randint(0,len(values)-1)] + ","
    return record[:-1]

def generate_dataset(size):
    parse_cat_values()
    if os.path.exists('data/health.data'):
        os.remove('data/health.data')
    data_file = open('data/health.data', 'w')    
    for i in range(size):
        record = ""
        for i in range(len(QI_INDEX)):
            if IS_CAT[i] is False:
                record += str(random.randint(0, MAX_VALUE[i])) + ","
            else:
                cat_values = VALUES[i]
                record += cat_values[random.randint(0,len(cat_values)-1)] + ","
        record = record[:len(record)-1]
        data_file.write(record + "\n")

def parse_cat_values():
    for i in range(len(QI_INDEX)):
        cat_values = []
        if IS_CAT[i] is True:
            with importlib.resources.path('basic_mondrian_health.data', 'health_' + ATT_NAMES[QI_INDEX[i]] + '.txt') as path:
                data_file = open(path)
                for line in data_file:
                    line = line.strip()
                    if len(line) == 0 or '?' in line:
                        continue
                    line = line.replace(' ', '')
                    cat_values.append(line.split(';')[0])
            VALUES.append(cat_values)

if __name__ == '__main__':
    generate_dataset(100)