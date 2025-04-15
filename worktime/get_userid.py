from tools import iheader, env
import requests
import json


url = "https://hub.sdxnetcafe.com/api/admin/salary/user/list?branchId=a92fd8a33b7811ea87766c92bf5c82be"

response = requests.get(url , headers=iheader.headers, timeout=10)

if (response.reason=='OK'):
    response_usrId = response.json()
else:
    print('请求userinfo失败，检查token是否过期')


def togethor(response_json):
    userIDs={}
    for item in response_json['data']:
        userIDs[item['name']] = item['id']
    return userIDs

try:
    userids  = togethor(response_usrId)

    with open(f'{env.proj_dir}/worktime/userIDs.json', 'w') as cache:
        json.dump(userids, cache, ensure_ascii=False, indent=4)
except Exception as e:
    print("togethor failed!",e)

if __name__ == "__main__":
    print("response_usrId, from get_userid,",response_usrId)
    print('userid',userids)
