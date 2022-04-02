'''
Author: Delsart
Date: 2022-03-16 22:35:14
LastEditTime: 2022-04-02 10:04:03
Description: 
FilePath: \SWU-auto-check\GetLocation.py
URL: https://github.com/Delsart/SWU-auto-check/blob/main/GetLocation.py
'''
import time
import MyRequest
import json
import os
key = 'fa202a1bc106133069eecbf7304dae99'
url = 'https://restapi.amap.com/v3/geocode/geo'

session = MyRequest.MySession()

def getFormedLoaction(address_text):
    with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'Location.json'),'r',encoding='utf8') as load_f:
        geo_formate = json.load(load_f)
    res = session.get(url=url, params={'key': key, 'address': address_text})
    geocodes=res.json()['geocodes'][0]
    geo_formate['address']=address_text
    geo_formate['province']=geocodes['province']
    geo_formate['district']=geocodes['district']
    geo_formate['road']=geocodes['street']
    geo_formate['time']=int(time.time())
    geo_formate['longitude']=geocodes['location'].split(',')[0]
    geo_formate['latitude']=geocodes['location'].split(',')[0]
    print('\nlocation >>>\n'+str(geo_formate))
    return geo_formate


# getFormedLoaction('重庆市北碚区文渊路2号靠近西南大学桃园园区文化广场')
