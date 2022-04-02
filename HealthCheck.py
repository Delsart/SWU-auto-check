'''
Author: Delsart
Date: 2022-01-12 22:17:58
LastEditTime: 2022-04-02 10:04:05
Description: health check
FilePath: \SWU-auto-check\HealthCheck.py
URL: https://github.com/Delsart/SWU-auto-check/blob/main/HealthCheck.py
'''


import MyRequest
import json
import os
import Login 
import GetLocation


student_id=''
passwd=''



form_id = '3fc165a338ee4450966268383da9a007'
def getPayLoad(form_id, data_id, session, headers, student_id):
    params = {'dataId': data_id, 'formId': form_id}
    res = session.get(url=f"http://counselor.swu.edu.cn/gateway//fighter-workflow/form-instance/select",
                      headers=headers, params=params)
    payload = res.json()['data']

    # payload['dksj']=time.strftime("%Y-%m-%d %H:%M", time.localtime())
    payload['formId'] = form_id

    res = session.get(url=f" http://counselor.swu.edu.cn/gateway/fighter-workflow/jkdk/pageDkxxByXh?",
                      headers=headers, params={'pageNum': 1, 'pageSize': 30, 'xh': student_id})
    for item in res.json()['data']['records']:
        if item['dkzt'] == '已打卡':
            payload['dkdd'] = GetLocation.getFormedLoaction(item['dkdd'])
            break

    res = session.get(url=f"http://counselor.swu.edu.cn/gateway/fighter-workflow/form-instance/default-data-collection",
                      headers=headers, params={'formId': form_id})
    for item in res.json()['data']['column']:
        prop = item['prop']
        if payload.get(prop, '') == '' and 'value' in item:
            payload[prop] = item['value']

    print(f"\npayload >>>\n {payload}")
    return payload


def launch_health_check(student_id, password):
    fighter_auth_token = Login.getFighterAuthToken(student_id, password)

    session = MyRequest.MySession()
    with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'Headers.json'), 'r', encoding='utf8') as load_f:
        headers = json.load(load_f)
    headers['fighter-auth-token'] = fighter_auth_token

    res = session.get(url=f"http://counselor.swu.edu.cn/gateway/fighter-workflow/jkdk/getIntradayDKXX",
                      headers=headers, params={'xh': student_id})

    for record in res.json()['data']:
        payload = getPayLoad(
            form_id, record['id'], session, headers, student_id)
        res = session.post(url=f"http://counselor.swu.edu.cn/gateway//fighter-workflow/form-instance/save",
                           headers=headers, params={'formId': form_id}, data=json.dumps(payload))
        print(res.json())
        if not res.json()['code'] == 200:
            return False
    return True

print(launch_health_check(student_id,passwd))
