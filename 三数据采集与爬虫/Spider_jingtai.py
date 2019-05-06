#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 21:12
# @Author  : Paulson
# @File    : Spider_jingtai.py
# @Software: PyCharm
# @define  : function


import random
import time

import pandas as pd
import requests
from lxml import etree

# 真实cookie
# Cookie = 'user_trace_token=20190312230635-bd10a4e8-55d7-48b5-962d-f9227b07ccd4; _ga=GA1.2.434082682.1552403204; LGUID=20190312230642-71a19b72-44d8-11e9-946e-5254005c3644; JSESSIONID=ABAAABAAAIAACBIDC1DB26FED5F93A2A2B73CA1A5C421FD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557148390; LGSID=20190506211309-b17281e3-7000-11e9-8664-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.1330006640.1557148395; TG-TRACK-CODE=index_search; LG_LOGIN_USER_ID=c6ffaba7ee92122f4b041f9a849d4f9d924b7edf620798a600169b4fff1a9f6d; LG_HAS_LOGIN=1; _putrc=5F44CFCCC08C9A2A123F89F2B170EADC; login=true; unick=%E9%AD%8F%E5%85%83%E5%AE%9D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=33; gate_login_token=9906db5b022596f1e3c42a1a991e55e88620b336119a01db8145d3c90d65c1be; X_MIDDLE_TOKEN=411fdb1739a24c8cf116bd0c0a582ee8; SEARCH_ID=a5f8d93efba748ad9b3f3e7ff1aa0eb2; X_HTTP_TOKEN=d3a07b50a9f6063e1201517551a0b095c1f90e316f; _gat=1; LGRID=20190506215701-d25a77de-7006-11e9-8668-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557151022'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    # 'Cookie': Cookie
}


for i in range(1, 2):
    time.sleep(random.randint(3, 10))
    url = 'https://www.lagou.com/zhaopin/jiqixuexi/{}/?filterOption=2'.format(i)
    print(url)
    print('正在抓取第{}页数据...'.format(i))

    # 请求网页并解析
    con = etree.HTML(requests.get(url, headers=headers).text)

    # 使用xpath表达式抽取各个字段信息
    job_name = [i for i in con.xpath('//a[@class="position_link"]/h3/text()')]
    print(job_name)
    job_address = [i for i in con.xpath("//a[@class='position_link']/span/em/text()")]
    job_company = [i for i in con.xpath("//div[@class='company_name']/a/text()")]
    job_salary = [i for i in con.xpath("//span[@class='money']/text()")]
    job_exp_edu = [i for i in con.xpath("//div[@class='li_b_l']/text()")]
    job_exp_edu2 = [i for i in [i.strip() for i in job_exp_edu] if i != '']
    job_industry = [i for i in con.xpath("//div[@class='industry']/text()")]
    job_tempation = [i for i in con.xpath("//div[@class='list_item_bot']/div[@class='li_b_r']/text()")]
    job_links = [i for i in con.xpath("//div[@class='p_top']/a/@href")]
    print(job_links)
    # 获取详情页链接后采集详情页岗位描述信息
    job_des = []
    for link in job_links:
        time.sleep(random.randint(3, 10))
        con2 = etree.HTML(requests.get(url=link, headers=headers).text)
        des = [[i.xpath('string(.)') for i in con2.xpath("//dd[@class='job_bt']/div/p")]]
        print(des)
        job_des += des

# 对数据进行字典封装
    dataset = {
        '岗位名称': job_name,
        '工作地址': job_address,
        '公司': job_company,
        '薪资': job_salary,
        '经验学历': job_exp_edu2,
        '所属行业': job_industry,
        '岗位福利': job_tempation,
        '任职要求': job_des
    }

# 转化为数据框并存为csv
    data = pd.DataFrame(dataset)
    data.to_csv('machine_learning_hz_job2.csv')