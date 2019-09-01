#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 20:57
# @Author  : Paulson
# @File    : data_clear.py
# @Software: PyCharm
# @define  : function

# import numpy as np
import pandas as pd
# import string
import warnings

warnings.filterwarnings('ignore')


class data_clean(object):
    def __init__(self):
        pass

    def get_data(self):
        data = pd.read_csv('./data_analysis.csv')
        return data

    def clean_operation(self):
        data = self.get_data()
        data['address'] = data['address'].fillna("['未知']")
        for i, j in enumerate(data['address']):
            j = j.replace('[', '').replace(']', '')
            data['address'][i] = j

        for i, j in enumerate(data['salary']):
            j = j.replace('k', '').replace('K', '').replace('以上', '-0')
            j1 = int(j.split('-')[0])
            j2 = int(j.split('-')[1])
            j3 = 1 / 2 * (j1 + j2)
            data['salary'][i] = j3 * 1000

        for i, j in enumerate(data['industryLables']):
            j = j.replace('[', '').replace(']', '')
            data['industryLables'][i] = j

        for i, j in enumerate(data['label']):
            j = j.replace('[', '').replace(']', '')
            data['label'][i] = j

        data['position_detail'] = data['position_detail'].fillna('未知')
        #         for i, j in enumerate(data['position_detail']):
        #             j = j.replace('\r', '')
        #             data['position_detail'][i] = j

        return data


opt = data_clean()
data = opt.clean_operation()
data.head()
