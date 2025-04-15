import requests
import json
from datetime import datetime, timedelta, date
import pytz
import argparse

from tools import env, logger

#loger = logger.get_logger(name='meituan', log_file=f'{env.proj_dir}/meituan/log')
logger = logger.get_logger(__name__)

cookies  = env.configjson['cookies']['mt']
proj_dir = env.proj_dir

from urllib.parse import unquote

mt_status   = 0
scheme      = 'https://'
hostname    = 'e.dianping.com'
url_path    = '/couponrecord/queryCouponRecordDetails'
params  = {
    'yodaReady'     : 'h5',
    'csecplatform'  : 4,
    'csecversion'   : 3.1,
    'mtgsig'        :  {"a1":"1.2",
               "a2":1741649588314,
               "a3":"1740084568043CAMCCCC2960edaad10e294fa6f28397fe2285903389",
               "a5":"Stv5DY8JgwkU6K8t4Du0kW28bQkLXNubi56yxynYvGXmMreHk QD=",
               "a6":"hs1.6h/L/xOLbp6kZFEDQEAObwkld84/kTqS1g1ljpf6mKulGU6ne9JVuPJdL3LBb3lXNOqAWDnQsCsrrgN1VbGtpQ6KFddNpdWZhbJyHp9BouTHef3eztuAH/r+z8iKD5o8z",
               "a8"
:"d4cec0195eb597922168c13086f2db17",
               "a9":"3.1.0, 7,77",
               "a10":"e4",
               "x0":4,
               "d1":"f9ac135a402fd1f6a9965235b983c2a0"}

}

url = f'{scheme}{hostname}{url_path}'

originurl = f'''
    ?=h5&
    csecplatform=4&
    csecversion=3.1.0&
    mtgsig=%7B%22a1%22%3A%221.2%22%2C%22a2%22%3A1741649588314%2C%22a3%22%3A%221740084568043CAMCCCC2960edaad10e294fa6f28397fe2285903389%22%2C%22a5%22%3A%22Stv5DY8JgwkU6K8t4Du0kW28bQkLXNubi56yxynYvGXmMreHkQD%3D%22%2C%22a6%22%3A%22hs1.6h%2FL%2FxOLbp6kZFEDQEAObwkld84%2FkTqS1g1ljpf6mKulGU6ne9JVuPJdL3LBb3lXNOqAWDnQsCsrrgN1VbGtpQ6KFddNpdWZhbJyHp9BouTHef3eztuAH%2Fr%2Bz8iKD5o8z%22%2C%22a8%22%3A%22d4cec0195eb597922168c13086f2db17%22%2C%22a9%22%3A%223.1.0%2C7%2C77%22%2C%22a10%22%3A%22e4%22%2C%22x0%22%3A4%2C%22d1%22%3A%22f9ac135a402fd1f6a9965235b983c2a0%22%7D
    '''

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "*/*",
    "Accept-Language": "zh,en-US;q=0.7,en;q=0.3",
    "Content-Type": "application/json",
    "Origin": "https://e.dianping.com",
    "Referer": "https://e.dianping.com/app/np-mer-voucher-web-static/records",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
}

def get_meituanSum(date):
    #date: <datetime.datetime>对象
    today_start = datetime(date.year, date.month, date.day)
    today_end = today_start + timedelta(hours=23, minutes=59, seconds=59)
    logger.info(f'美团数据日期{today_end}')
    # 转换为 Unix 时间戳（单位：秒）
    begin_timestamp = int(today_start.timestamp()*1000)
    end_timestamp = int(today_end.timestamp()*1000)

    data = {
        "selectDealId": 0,
        "bussinessType": 0,
        "selectShopId": 1340799757,
        "productTabNum": 1,
        "offset": 0,
        "limit": 20,
        "beginDate": begin_timestamp,
        "endDate": end_timestamp,
        "subTabNum": None
    }
    response = requests.post(url,params = params, headers=headers, json=data, cookies=cookies)
    json_data = response.json()

    with open(f"{proj_dir}/meituan/meituan.json",'w') as data_json:
        json.dump(response.json(), data_json, ensure_ascii=False, indent=4)

    sale_price_sum = 0
    couponRecordDetails = json_data["data"]["couponRecordDetails"]

    if  couponRecordDetails:           
        for record in couponRecordDetails:
            price = record["salePrice"]
            print(price)
            sale_price = price.replace("¥", "")  # 去除货币符号
            print(sale_price)
            sale_price_sum += float(sale_price)
            sale_price_sum = round(sale_price_sum, 2) 
    return sale_price_sum

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="美团组件")
    parser.add_argument("-n", "--now", action="store_true", help="今天的数据")
    args = parser.parse_args()
    yesterday =datetime.today()-timedelta(days=1) 
    mtsum = get_meituanSum(yesterday)
    logger.info(f'美团数据{yesterday}: {mtsum}')
