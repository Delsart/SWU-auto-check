'''
Author: Delsart
Date: 2022-01-12 22:17:58
LastEditTime: 2022-04-02 10:04:02
Description: dorm check
FilePath: \SWU-auto-check\DormCheck.py
URL: https://github.com/Delsart/SWU-auto-check/blob/main/DormCheck.py
'''


import time
import os
import json
import MyRequest
import Login

student_id=''
passwd=''



def getPayLoad(form_id,data_id, session, headers, student_id):

    res = session.post(url=f"http://counselor.swu.edu.cn/gateway/fighter-workflow/cqtj/getTransition",
                       headers=headers, params={'pageNum': 1, 'pageSize': 5})

    for record in res.json()['data']['records']:
        if record['qdzt']=='已签到':
            data_id_temp=record['id']
            break
    res = session.get(url=f"http://counselor.swu.edu.cn/gateway//fighter-workflow/form-instance/select",
                      headers=headers, params={'dataId': data_id_temp, 'formId': form_id})
    payload = res.json()['data']
    payload['tsrq'] = time.strftime("%Y-%m-%d", time.localtime())
    payload['id'] = data_id
    print(f"\npayload >>>\n {payload}")
    return payload


def launch_dorm_check(student_id, password):
    try:
        session = MyRequest.MySession()
        fighter_auth_token = Login.getFighterAuthToken(student_id, password)

        with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'Headers.json'), 'r', encoding='utf8') as load_f:
            headers = json.load(load_f)
        headers['fighter-auth-token'] = fighter_auth_token

        res = session.post(url=f"http://counselor.swu.edu.cn/gateway/fighter-workflow/cqtj/getTransitionByToday",
                        headers=headers, params={'pageNum': 1, 'pageSize': 5})

        for record in res.json()['data']['records']:
            payload = getPayLoad(record['formId'],record['id'], session, headers, student_id)
            res = session.post(url=f"http://counselor.swu.edu.cn/gateway//fighter-workflow/form-instance/save",
                            headers=headers, params={'formId': record['formId']}, data=json.dumps(payload))
            print(res.json())
            if res.json()['code'] == 200:
                return [True,'']
            return [False,res.json()]
    except Exception as ins:
        return [False,str(ins)]



print(launch_dorm_check(student_id,passwd))
