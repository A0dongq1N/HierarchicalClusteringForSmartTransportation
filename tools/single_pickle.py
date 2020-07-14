#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""单个对象的序列化和反序列化"""

__author__ = 'Aodongq1n'

import pickle


def save_object(obj, filename):
    with open(filename, 'wb') as output_file:
        pickle.dump(obj, output_file, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as input_file:
        obj = pickle.load(input_file)
    return obj


if __name__ == '__main__':
    pass
    # save_object(UserScheduleGroup(), '../data/usg.pkl')
