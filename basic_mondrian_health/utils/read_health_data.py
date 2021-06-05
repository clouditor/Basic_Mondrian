#!/usr/bin/env python
# coding=utf-8

from basic_mondrian_health.models.gentree import GenTree
from basic_mondrian_health.models.numrange import NumRange
from basic_mondrian_health.utils.utility import cmp_str
import pickle
import importlib

import pdb

ATT_NAMES = ['group', 'timestamp', 'medication', 'medication_dosage', 'symptom', 'symptom_strength']
QI_INDEX = [0, 1, 2, 3, 4, 5]
IS_CAT = [True, True, True, False, True, False]
SA_INDEX = -1

__DEBUG = False


def read_data():
    """
    read microda for *.txt and return read data
    """
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    for i in range(QI_num):
        numeric_dict.append(dict())
    # order categorical attributes in intuitive order
    # here, we use the appear number
    # data_file = open('data/health.data', 'rU')
    with importlib.resources.path('basic_mondrian_health.data', 'health.data') as path:
        with open(path, 'rU') as data_file:
            for line in data_file:
                line = line.strip()
                # remove empty and incomplete lines
                # only 30162 records will be kept
                if len(line) == 0 or '?' in line:
                    continue
                # remove double spaces
                line = line.replace(' ', '')
                temp = line.split(',')
                ltemp = []
                for i in range(QI_num):
                    index = QI_INDEX[i]
                    if IS_CAT[i] is False:
                        try:
                            numeric_dict[i][temp[index]] += 1
                        except KeyError:
                            numeric_dict[i][temp[index]] = 1
                    ltemp.append(temp[index])
                # ltemp.append(temp[SA_INDEX])
                data.append(ltemp)
            # pickle numeric attributes and get NumRange
            for i in range(QI_num):
                if IS_CAT[i] is False:
                    with importlib.resources.path('basic_mondrian_health.data', 'health_' + ATT_NAMES[QI_INDEX[i]] + '_static.pickle') as path:
                        static_file = open(path, 'wb')
                        # static_file = open('data/health_' + ATT_NAMES[QI_INDEX[i]] + '_static.pickle', 'wb')
                        sort_value = list(numeric_dict[i].keys())
                        sort_value = sorted(sort_value, key=int)
                        pickle.dump((numeric_dict[i], sort_value), static_file)
                        static_file.close()
            return data


def read_tree():
    """read tree from data/tree_*.txt, store them in att_tree
    """
    att_names = []
    att_trees = []
    for t in QI_INDEX:
        att_names.append(ATT_NAMES[t])
    for i in range(len(att_names)):
        if IS_CAT[i]:
            att_trees.append(read_tree_file(att_names[i]))
        else:
            att_trees.append(read_pickle_file(att_names[i]))
    return att_trees


def read_pickle_file(att_name):
    """
    read pickle file for numeric attributes
    return numrange object
    """
    try:
        with importlib.resources.path('basic_mondrian_health.data', 'health_' + att_name + '_static.pickle') as path:
            static_file = open(path, 'rb')
        (numeric_dict, sort_value) = pickle.load(static_file)
    except:
        print("Pickle file not exists!!")
    static_file.close()
    result = NumRange(sort_value, numeric_dict)
    return result


def read_tree_file(treename):
    """read tree data from treename
    """
    leaf_to_path = {}
    att_tree = {}
    prefix = 'health_'
    postfix = ".txt"
    with importlib.resources.path('basic_mondrian_health.data', prefix + treename + postfix) as path:
        treefile = open(path, 'rU')
    att_tree['*'] = GenTree('*')
    if __DEBUG:
        print("Reading Tree" + treename)
    for line in treefile:
        # delete \n
        if len(line) <= 1:
            break
        line = line.strip()
        temp = line.split(';')
        # copy temp
        temp.reverse()
        for i, t in enumerate(temp):
            isleaf = False
            if i == len(temp) - 1:
                isleaf = True
            # try and except is more efficient than 'in'
            try:
                att_tree[t]
            except:
                att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)
    if __DEBUG:
        print("Nodes No. = %d" % att_tree['*'].support)
    treefile.close()
    return att_tree
