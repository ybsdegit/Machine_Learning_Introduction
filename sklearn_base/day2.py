#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 21:01
# @Author  : Paulson
# @File    : day2.py
# @Software: PyCharm
# @define  : function

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, fetch_20newsgroups, load_boston
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# li = load_iris()

# print('获取特征值')
# print(li.data)
# print('目标值')
# print(li.target)
# print(li.DESCR)

# 注意返回值，训练集train x_train(特征值）, y_train(目标值)，测试集test x_text， y_text
# x_train, x_test, y_train, y_test = train_test_split(li.data, li.target, test_size=0.25)
# print("训练集特征值和目标值：", x_train, y_train)
# print("测试集特征值和目标值：", x_test, y_test)

# news = fetch_20newsgroups(subset='all')
# print(news.data)
# print(news.target)
# lb = load_boston()
# print(lb.data)
# print('目标值')
# print(lb.target)
# print(lb.DESCR)


def knncls():
    """
    K-近邻预测用户签到位置
    :return: None
    """
    # 一、读取数据
    data = pd.read_csv('./data/facebook/train.csv')
    # print(data.head(10))
    
    # 二、处理数据
    # 1、缩小数据范围, 查询数据筛选
    data = data.query("x > 1.0 & x < 1.25 & y > 2.5 & y < 2.75")
    # 2、处理时间的数据
    time_value = pd.to_datetime(data['time'], unit='s')
    # print(time_value)
    # 构造新的特征,把日期格式转换成字典格式
    time_value = pd.DatetimeIndex(time_value)
    data['day'] = time_value.day
    data['hour'] = time_value.hour
    data['weekday'] = time_value.weekday
    
    # 把时间戳特征、row_id特征删除
    data = data.drop(['time'], axis=1)  # 按列删除 pandas 1 表示列
    # print(data.head(10))
    
    # 把签到数据少于n个的目标位置删除
    place_count = data.groupby('place_id').count()  # 建立索引
    tf = place_count[place_count.row_id > 3].reset_index()  # 把次数大于3的保留
    data = data[data['place_id'].isin(tf.place_id)]
    # print(data.head(10))
    
    # 取出数据当中的特征值和目标值
    y = data['place_id']  # 目标值
    x = data.drop(['place_id'], axis=1)  # 特征值
    data = data.drop(['row_id'], axis=1)  # 按列删除 pandas 1 表示列
    print(data)
    
    # 进行数据分割 数据集、测试集
    # 训练集特征值，测试集特征值，训练集目标值，测试集目标值
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    
    # 三、特征工程（标准化）
    std = StandardScaler()
    # 对测试集和训练集的特征值进行标准化
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)
    
    # 四、进行算法流程
    knn = KNeighborsClassifier()
    
    # # fit, predict, score
    # knn.fit(x_train, y_train)
    #
    # # 得出预测结果
    # y_predict = knn.predict(x_test)
    # print('预测的目标签到位置为：', y_predict)
    #
    # # 得出准确率 测试集特征值，测试集目标值
    # print('预测的准确率为：', knn.score(x_test, y_test))
    
    # 进行网格搜素
    # 构造一些参数的值进行搜素
    param = {"n_neighbors": [3, 5 ,10, 15, 20]}
    gc = GridSearchCV(knn, param_grid=param, cv=2)
    gc.fit(x_train, y_train)
    
    # 预测准确率
    print('在测试集上的准确率', gc.score(x_test, y_test))
    
    print('在交叉验证中最好的结果：', gc.best_score_)
    print('选择了最好的模型是： ', gc.best_estimator_)
    print('每个超参数每次交叉验证的结果： ', gc.cv_results_)
    
    
    return None


def naviebayes():
    """
    朴素贝叶斯进行文本分类
    :return: None
    """
    news = fetch_20newsgroups(subset='all')
    
    # 进行数据分割
    x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)
    
    # 对数据集进行特征抽取
    tf = TfidfVectorizer()
    
    # 以训练集当中的词的列表进行每篇文章重要性统计['a', 'b', 'c']
    x_train = tf.fit_transform(x_train)
    # print(tf.get_feature_names())
    x_test = tf.transform(x_test)
    
    # 进行朴素贝叶斯算法的预测
    mlt = MultinomialNB(alpha=1.0)
    print(x_train.toarray())
    mlt.fit(x_train, y_train)
    y_predict = mlt.predict(x_test)
    print('预测的文章类别为：', y_predict)
    # 得出准确率 测试集特征值，测试集目标值
    print('预测的准确率为：', mlt.score(x_test, y_test))
    print("每个类别的精确率和召回率：" , classification_report(y_test, y_predict, target_names=news.target_names))


if __name__ == '__main__':
    knncls()
    # naviebayes()
