import random
import os

ATT_NAMES = ['age', 'zip', 'sex', 'symptom']
QI_INDEX = [0, 1, 2, 3]
IS_CAT = [False, False, True, True]
MAX_VALUE = [120,99999]
VALUES = []

def parse_cat_values():
    for i in range(len(QI_INDEX)):
        cat_values = []
        if IS_CAT[i] is True:
            data_file = open('data/health_' + ATT_NAMES[QI_INDEX[i]] + '.txt', 'r')
            for line in data_file:
                line = line.strip()
                if len(line) == 0 or '?' in line:
                    continue
                line = line.replace(' ', '')
                cat_values.append(line.split(';')[0])
        VALUES.append(cat_values)


def generate_one_record():
    record = ""
    for i in range(len(QI_INDEX)):
        if IS_CAT[i] is False:
            record += str(random.randint(0, MAX_VALUE[i])) + ","
        else:
            data_file = open('data/health_' + ATT_NAMES[QI_INDEX[i]] + '.txt', 'r')
            values = []
            for line in data_file:
                line = line.strip()
                if len(line) == 0 or '?' in line:
                    continue
                line = line.replace(' ', '')
                temp = line.split(';')
                values.append(temp[0])
            record += values[random.randint(0,len(values)-1)] + ","
    print(record)

def generate_dataset(size):
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

if __name__ == '__main__':
    # generate_one_record()
    parse_cat_values()
    print(VALUES)
    generate_dataset(100)