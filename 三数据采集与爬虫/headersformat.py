headers = """
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Cookie: user_trace_token=20190312230635-bd10a4e8-55d7-48b5-962d-f9227b07ccd4; _ga=GA1.2.434082682.1552403204; LGUID=20190312230642-71a19b72-44d8-11e9-946e-5254005c3644; JSESSIONID=ABAAABAAAIAACBIDC1DB26FED5F93A2A2B73CA1A5C421FD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557148390; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.1330006640.1557148395; LG_LOGIN_USER_ID=c6ffaba7ee92122f4b041f9a849d4f9d924b7edf620798a600169b4fff1a9f6d; LG_HAS_LOGIN=1; _putrc=5F44CFCCC08C9A2A123F89F2B170EADC; login=true; unick=%E9%AD%8F%E5%85%83%E5%AE%9D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=33; gate_login_token=9906db5b022596f1e3c42a1a991e55e88620b336119a01db8145d3c90d65c1be; X_MIDDLE_TOKEN=411fdb1739a24c8cf116bd0c0a582ee8; TG-TRACK-CODE=search_code; SEARCH_ID=edea9ba44bc9459db8eb58ec279ca51b; X_HTTP_TOKEN=d3a07b50a9f6063e2803517551a0b095c1f90e316f; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1557153083; LGRID=20190506223122-9eb78021-700b-11e9-8688-525400f775ce
Host: www.lagou.com
Referer: https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?labelWords=&fromSearch=true&suginput=
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36
"""
hs = headers.split('\n')
b = [k for k in hs if len(k)]
e = b
f = {(i.split(":")[0], i.split(":", 1)[1].strip()) for i in e}
g = sorted(f)
index = 0
print("{")
for k, v in g:
    print(repr(k).replace('\'', '"'), repr(v).replace('\'', '"'), sep=':', end=",\n")
print("}")