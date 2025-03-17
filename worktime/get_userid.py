from tools import iheader
import requests

url = "https://hub.sdxnetcafe.com/api/admin/salary/user/list?branchId=a92fd8a33b7811ea87766c92bf5c82be"

response = requests.get(url , headers=iheader.headers)

data = response.json()
userIDs={}
for item in data['data']:

    userIDs[item['name']] = item['id']


