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