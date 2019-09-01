#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 22:11
# @Author  : Paulson
# @File    : Spider_dongtai.py
# @Software: PyCharm
# @define  : function


import json
import random
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

#定义抓取主函数
def lagou_dynamic_crawl():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    # 创建一个职位列表容器
    positions = []
    for page in range(1, 31):
        print('正在抓取{}页数据...'.format(page))
        URL_ = 'https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        URL = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        # 构建请求保单参数
        params = {
            'first': 'false',
            'pn': page,
            'kd': '机器学习'
        }

        # 构造请求并返回结果
        s = requests.Session()
        s.get(URL_, headers=headers, timeout=3)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        result = s.post(URL, headers=headers, data=params, cookies=cookie, timeout=3)
        print(result.text)

        # 将请求结果转化为json
        json_result = result.json()

        # 解析json数据获取目标信息
        try:
            position_info = json_result['content']['positionResult']['result']
        except:
            position_info = json_result['msg']
            if '您操作太频繁' in position_info:
                print('操作太频繁')
                assert False

        # 循环当前页每一个职位信息，再去爬职位详情页面
        for position in position_info:
            # 把我们要爬取的信息放入字典
            position_dict = {
                'position_name': position['positionName'],
                'work_year': position['workYear'],
                'education': position['education'],
                'salary': position['salary'],
                'city': position['city'],
                'company_name': position['companyFullName'],
                'address': position['businessZones'],
                'label': position['companyLabelList'],
                'stage': position['financeStage'],
                'size': position['companySize'],
                'advantage': position['positionAdvantage'],
                'industry': position['industryField'],
                'industryLables': position['industryLables']
            }
            # 找到职位id
            position_id = position['positionId']

            # 根据职位id调用岗位描述函数获取职位描述

            position_dict['position_detail'] = recruit_detail(position_id)
            positions.append(position_dict)

        time.sleep(random.randint(3, 6))
    print('全部数据采集完毕...')
    return positions

# 定义抓取岗位描述函数
def recruit_detail(position_id):
    headers = {
        # "Cookie": "user_trace_token=20190312230635-bd10a4e8-55d7-48b5-962d-f9227b07ccd4; _ga=GA1.2.434082682.1552403204; LGUID=20190312230642-71a19b72-44d8-11e9-946e-5254005c3644; JSESSIONID=ABAAABAAAIAACBIDC1DB26FED5F93A2A2B73CA1A5C421FD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557148390; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.1330006640.1557148395; LG_LOGIN_USER_ID=c6ffaba7ee92122f4b041f9a849d4f9d924b7edf620798a600169b4fff1a9f6d; LG_HAS_LOGIN=1; _putrc=5F44CFCCC08C9A2A123F89F2B170EADC; login=true; unick=%E9%AD%8F%E5%85%83%E5%AE%9D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=33; gate_login_token=9906db5b022596f1e3c42a1a991e55e88620b336119a01db8145d3c90d65c1be; X_MIDDLE_TOKEN=411fdb1739a24c8cf116bd0c0a582ee8; TG-TRACK-CODE=search_code; SEARCH_ID=edea9ba44bc9459db8eb58ec279ca51b; X_HTTP_TOKEN=d3a07b50a9f6063e2803517551a0b095c1f90e316f; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557153083; LGRID=20190506223122-9eb78021-700b-11e9-8688-525400f775ce",
        "Host": "www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?labelWords=&fromSearch=true&suginput=",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }
    url = 'https://www.lagou.com/jobs/%s.html' % position_id
    result = requests.get(url, headers=headers)
    time.sleep(random.randint(1, 4))

    # 解析职位要求text
    soup = BeautifulSoup(result.text, 'html.parser')
    job_bt = soup.find(class_='job_bt')

    # 通过尝试发现部分记录描述存在空的情况
    # 所以这里需要判断处理一下
    if job_bt != None:
        job_bt = job_bt.text
    else:
        job_bt = 'null'
    print(job_bt)
    return job_bt


if __name__ == '__main__':
    positions = lagou_dynamic_crawl()
    data = pd.DataFrame(positions)
    data.to_csv('machine_learning_hz_job3.csv')
