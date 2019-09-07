#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 23:49
# @Author  : Paulson
# @File    : day3.py
# @Software: PyCharm
# @define  : function

import numpy as np
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.externals import joblib


def mylinear():
    """
    现行回归直接预测房屋价格
    :return: None
    """
    # 一、获取数据
    lb = load_boston()
    
    # 二、分割数据集到训练集、测试集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)
    # print(y_train, y_test)
    
    # 三、进行标准化处理(?) 目标值要不要进行标准化处理？需要
    # 特征值和目标值都必须进行标准化,实例化2个标准化Api
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    
    # 目标值
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))  # 二维
    y_test = std_y.transform(y_test.reshape(-1, 1))
    
    # 四、estimator预测
    # 正规方程求解方式预测结果
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    print("回归系数", lr.coef_)
    
    # 保存训练好的模型
    # joblib.dump(lr, "./temp/test.pkl")
    
    # 使用训练好的模型训练
    modle = joblib.load('./temp/test.pkl')
    y_predict = std_y.inverse_transform(modle.predict(x_test))
    print("保存的模型预测的结果", y_predict)

    # 预测测试集的房子价额
    y_r_predict = std_y.inverse_transform(lr.predict(x_test))
    # print("正规方程测试集里面每个房子的预测价格是： ", y_r_predict)
    print("正规方程的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), y_r_predict))
    
    # 梯度下降去进行房价预测
    sgd = SGDRegressor()
    sgd.fit(x_train, y_train)
    print("回归系数", sgd.coef_)
    # 预测测试集的房子价额
    y_sgd_predict = std_y.inverse_transform(sgd.predict(x_test))
    # print("梯度下降测试集里面每个房子的预测价格是： ", y_sgd_predict)
    print("梯度下降的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), y_sgd_predict))
    
    # 岭回归下降去进行房价预测
    rd = Ridge(alpha=1.0)
    rd.fit(x_train, y_train)
    print("回归系数", rd.coef_)
    # 预测测试集的房子价额
    y_rd_predict = std_y.inverse_transform(rd.predict(x_test))
    # print("岭回归测试集里面每个房子的预测价格是： ", y_rd_predict)
    print("岭回归的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), y_rd_predict))
    
    return None


def logistic():
    """
    逻辑回归做二分类进行癌症预测（根据细胞的属性特征）
    :return: None
    """
    # 构造列标签名
    column = ['Sample code number', 'Clump Thickness',
              'Uniformity of Cell Size', 'Uniformity of Cell Shape',
              'Marginal Adhesion', 'Single Epithelial Cell Size',
              'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']
    
    # 读取数据
    data = pd.read_csv('./data/breast-cancer-wisconsin.data', names=column)
    print(data)
    
    # 缺失值处理
    data = data.replace(to_replace='?', value=np.nan)
    data = data.dropna()
    
    # 进行数据的分割
    x_train, x_test, y_train, y_test = train_test_split(data[column[1:10]], data[column[10]], test_size=0.25)
    
    # 进行标准化处理
    std = StandardScaler()
    std.fit_transform(x_train)
    std.transform(x_test)
    
    # 逻辑回归预测
    lg = LogisticRegression(C=1.0)
    lg.fit(x_train, y_train)
    
    print(lg.coef_)
    y_predict = lg.predict(x_test)
    print("准备率：", lg.score(x_test, y_test))
    
    print('召回率：\n', classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "恶性"]))
    
    return None

if __name__ == '__main__':
    # mylinear()
    logistic()
