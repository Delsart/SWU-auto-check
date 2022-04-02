'''
Author: Delsart
Date: 2022-01-13 09:39:06
LastEditTime: 2022-04-02 10:03:01
Description: login and get figther-auth-token
FilePath: \SWU-auto-check\Login.py
URL: https://github.com/Delsart/SWU-auto-check/blob/main/Login.py
'''
import MyRequest
from bs4 import BeautifulSoup
from urllib import parse


payload_attr = {'lt', 'execution', '_eventId', 'isQrSubmit', 'qrValue'}
session = MyRequest.MySession()

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-CN; HD1910 Build/QKQ1.190716.003) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.22.1.161 Mobile Safari/537.36 AliApp(DingTalk/6.3.20) com.alibaba.android.rimet/22556827 Channel/227200 language/zh-CN abi/32 UT4Aplus/0.2.25 colorScheme/light',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
}


def getPayload(text_res):
    res = {}
    for s in BeautifulSoup(text_res, "html.parser").find_all('input'):
        if s.attrs['name'] in payload_attr:
            res[s.attrs['name']] = s.attrs['value']
    return res


def login(username,passwd):
    url = 'https://uaaap.swu.edu.cn/cas/login'
    res = session.post(url=url, headers=headers)
    payload = getPayload(res.text)
    payload['username'] = username
    payload['password'] = passwd
    print(f"\npayload >>>\n {payload}")
    session.post(url=url, headers=headers, data=parse.urlencode(payload))


def getFighterAuthToken(username,passwd):
    login(username,passwd)
    url = 'http://counselor.swu.edu.cn/gateway/fighter-integrate-uaap/integrate/uaap/cas/to-cas-login'
    headers['content-type'] = 'application/json'
    res = session.get(url=url, allow_redirects=True,
                      headers=headers, params={'next': '/index', 'thirdPartyName': '', 'frontUrl': 'http://counselor.swu.edu.cn/#/casLogin'})
    for item in res.history:
        if 'Fighter-Auth-Token' in item.headers:
            print(
                f"\nfighter-auth-token >>>\n {item.headers['Fighter-Auth-Token']}")
            return item.headers['Fighter-Auth-Token']
    raise Exception('no Fighter-Auth-Token')