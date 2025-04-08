from tools.iheader import headers as Iheaders
from tools import logger

import requests
import math
from datetime import datetime
from collections import defaultdict

logger=logger.get_logger('third_party')

raw_header = """ Host: hub.sdxnetcafe.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: application/json, text/plain, */*
Accept-Language: zh,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br, zstd
Content-Type: application/json;charset=utf-8
Content-Length: 107
Origin: https://hub.sdxnetcafe.com
Connection: keep-alive
Referer: https://hub.sdxnetcafe.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
"""
headers = {}
headers['Authorization'] =  Iheaders['Authorization']

lines = raw_header.splitlines()
for line in lines:
    # 跳过空行
    if line.strip():
        # 将每行按照第一个冒号拆分为键和值
        key, value = line.split(":", 1)
        # 去除键和值的多余空白，并添加到字典中
        headers[key.strip()] = value.strip()

url = 'https://hub.sdxnetcafe.com/api/admin/third/income/save'


#delete = f'https://hub.sdxnetcafe.com/api/admin/third/income/delete/{id}'
def get_list(page : int,limit : int, startTm=None, endTm=None):
    list_thirdpaty = f'https://hub.sdxnetcafe.com/api/admin/third/income/pageList?branchId=a92fd8a33b7811ea87766c92bf5c82be&startTm={startTm}&endTm={endTm}&page={page}&limit={limit}'
    response = requests.get(url = list_thirdpaty, headers=Iheaders, timeout=10, verify = True)
    response_list = response.json()
    return response_list


third_type_ids = defaultdict(list)
def gen_duplicated_item_dict(date_str, item_list):
    '''
    item_list<list>[<dicrt>]
    '''
    for item in  item_list:
        if item['reportDate'] == date_str:
            third_type = item['thirdType']
            item_id = item['id']
            third_type_ids[third_type].append(item_id)
            logger.warning('有重复的日期，需要删除')

def check_unique(date_str ):

    limit = 30
    startTm = date_str+' 00:00:00'
    endTm   = date_str+' 23:59:59'
    #调用函数获取列表
    response_list = get_list(page=1, limit=limit, startTm=startTm, endTm=endTm)
    logger.debug(f'重复的数据列表{response_list}')
    total  = response_list['data']['total']
    data_list = response_list['data']['rows']

    if total>limit:
        pages = math.cell(total/limit)
        for page in range(1,pages+1):
            response_list = get_list(page=page, limit=limit, startTm=startTm, endTm=endTm)
            logger.debug(f'重复的数据列表{response_list}')
            total  = response_list['data']['total']
            data_list = response_list['data']['rows']
            gen_duplicated_item_dict(date_str, data_list )

    else:
        gen_duplicated_item_dict(date_str, data_list )
    return third_type_ids  

def delete(id: str):

    delete = f'https://hub.sdxnetcafe.com/api/admin/third/income/delete/{id}'
    response = requests.get(url = delete,headers=Iheaders)

    if response.json()['status'] != 200:
        return 1
    else:
        logger.warning('删除成功')
        return 0
    return 0

def ota_update(ota_name,date_obj, income) :
    '''
        ota_name    <str>
        date_obj    <datetime.datetime> or <datetime.date>
        income      <int>
    '''
    logger.warning(f'正在更新{ota_name}的数据--------')
    date_str = date_obj.strftime("%Y-%m-%d")
    data  = {"branchId":"a92fd8a33b7811ea87766c92bf5c82be","reportDate":date_str,"thirdType":ota_name,"income":income}
    response = requests.post(url, headers=headers, json = data, timeout=10, verify = True)
    logger.info(f'更新操作的返回结果{response.text}')
    return response.json()
