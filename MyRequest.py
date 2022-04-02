'''
Author: Delsart
Date: 2022-01-12 19:23:04
LastEditTime: 2022-04-02 10:02:49
Description: 
FilePath: \SWU-auto-check\MyRequest.py
URL: https://github.com/Delsart/SWU-auto-check/blob/main/MyRequest.py
'''

import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 封装
class MySession:
    def __init__(self) -> None:
        self.session=requests.session()
    def getCookies(self) :
        return self.session.cookies
    def get(self,url,headers={},verify=False,params={},cookies=None, allow_redirects=False):
        count=0
        while True:
            try:
                if cookies:
                    return self.session.get(url,headers=headers,verify=verify,params=params, allow_redirects=allow_redirects,cookies=cookies)
                return self.session.get(url,headers=headers,verify=verify,params=params, allow_redirects=allow_redirects)
            except Exception as inst:
                count=count+1
                print(f"ERROR!\n\tget\n\turl:\t{url}\n\t{inst}\n\tretry:\t{count}")
                time.sleep(5)
    def head(self,url,headers={},verify=False,params={},cookies=None, allow_redirects=False):
        count=0
        while True:
            try:
                if cookies:
                    return self.session.head(url,headers=headers,verify=verify,params=params, allow_redirects=allow_redirects,cookies=cookies)
                return self.session.head(url,headers=headers,verify=verify,params=params, allow_redirects=allow_redirects)
            except Exception as inst:
                count=count+1
                print(f"ERROR!\n\thead\n\turl:\t{url}\n\t{inst}\n\tretry:\t{count}")
                time.sleep(5)

    def post(self,url,headers={},verify=False,params={},data={},files={},cookies=None):
        count=0
        while True:
            try:
                if cookies:
                    return self.session.post(url,headers=headers,verify=verify,params=params,data=data,files=files,cookies=cookies)
                return self.session.post(url,headers=headers,verify=verify,params=params,data=data,files=files)
            except Exception as inst:
                count=count+1
                print(f"ERROR!\n\tpost\n\turl:\t{url}\n\t{inst}\n\tretry\t{count}")
                time.sleep(5)