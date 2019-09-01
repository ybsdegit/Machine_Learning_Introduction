#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/28 0:26
# @Author  : Paulson
# @File    : day1.py
# @Software: PyCharm
# @define  : function
# from sklearn.feature_extraction.text import CountVectorizer
#
# # 实例化CountVectorizer
#
# vector = CountVectorizer()
#
# # 调用fit_transform输入并转换数据
#
# res = vector.fit_transform(["life is short,i like python","life is too long,i dislike python"])
#
# # 打印结果
# print(vector.get_feature_names())
# print(res.toarray())

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Imputer
from sklearn.decomposition import PCA
import numpy as np
import jieba


def dicvev():
    """
    字典数据抽取
    :return: None
    """
    
    data = [{'city': '北京', 'temperature': 100}, {'city': '上海', 'temperature': 60}, {'city': '深圳', 'temperature': 30}]
    # 实例化
    dict1 = DictVectorizer(sparse=False)
    data = dict1.fit_transform(data)
    
    print(dict1.get_feature_names())
    print(dict1.inverse_transform(data))
    print(data)
    
    
def countvec():
    """
    对文本进行特征值化
    :return: None
    """
    cv = CountVectorizer()
    # data = ["life is is short,i like python", "life is too long,i dislike python"]
    data = ["人生 短暂，我 喜欢 蟒蛇", "人生 太长，我 不喜欢 蟒蛇"]
    data = cv.fit_transform(data)
    # 统计所有文章当中所有的词，重复的之看做一次  词的列表
    # 对每篇文章，在词的列表里面进行统计每个词出现的次数
    print(cv.get_feature_names())
    print(data.toarray())
    return None


def cutword():
    con1 = jieba.cut("今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上，所以每个人不要放弃今天。")
    con2 = jieba.cut("我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。")
    con3 = jieba.cut("如果只用一种方式了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。")
    
    # 转换成列表
    content1 = list(con1)
    content2 = list(con2)
    content3 = list(con3)
    
    # 把列表转换成字符串，以空格隔开
    c1 = ' '.join(content1)
    c2 = ' '.join(content2)
    c3 = ' '.join(content3)
    
    return c1, c2, c3


def hanzivec():
    """
    中文特质值化
    :return: None
    """
    c1, c2, c3 = cutword()
    print(c1, c2, c3)
    cv = CountVectorizer()
    # data = ["life is is short,i like python", "life is too long,i dislike python"]
    data = cv.fit_transform([c1, c2, c3])
    # 统计所有文章当中所有的词，重复的之看做一次  词的列表
    # 对每篇文章，在词的列表里面进行统计每个词出现的次数
    print(cv.get_feature_names())
    print(data.toarray())
    return None


def tfidfvec():
    """
    文本分类 tf-idf
    :return: None
    """
    c1, c2, c3 = cutword()
    print(c1, c2, c3)
    tf = TfidfVectorizer()  # 重要性
    # data = ["life is is short,i like python", "life is too long,i dislike python"]
    data = tf.fit_transform([c1, c2, c3])
    # 统计所有文章当中所有的词，重复的之看做一次  词的列表
    # 对每篇文章，在词的列表里面进行统计每个词出现的次数
    print(tf.get_feature_names())
    print(data.toarray())
    return None


def mm():
    """
    归一化处理
    :return: None
    """
    data = [[90, 2, 10, 40], [60, 4, 15, 45], [75, 3, 13, 46]]

    # m = MinMaxScaler()
    m = MinMaxScaler(feature_range=(2, 3))
    data = m.fit_transform(data)
    print(data)
    return None
    

def stand():
    """
    标准化缩放
    :return: None
    """
    data = [[1., -1., 3.], [2., 4., 2.], [4., 6., -1.]]
    std = StandardScaler()
    data = std.fit_transform(data)
    print(data)
    return None
    

def im():
    """
    缺失值处理
    :return: None
    """
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)  # 0 按列填补
    data = imp.fit_transform([[1, 2], [np.nan, 3], [7, 6]])
    print(data)
    return None


def var():
    """
    特征选择-删除低方差的特征
    :return:
    """
    # va = VarianceThreshold()
    va = VarianceThreshold(threshold=1.0)
    data = va.fit_transform([[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]])
    print(data)
    return None


def pca():
    """
    主成分分析进行特征降维
    :return: None
    """
    pc = PCA(n_components=0.9)
    data = pc.fit_transform([[2,8,4,5], [6,3,0,8], [5,4,9,1]])
    print(data)
    return None
    
    

if __name__ == '__main__':
    # dicvev()
    # countvec()
    # hanzivec()
    # tfidfvec()
    # mm()
    # stand()
    # im()
    # var()
    pca()
