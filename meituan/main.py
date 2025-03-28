import requests
import json
import datetime
import pytz
import logging
import argparse

from tools import env, loger

loger = loger.get_logger(name='meituan', log_file=f'{env.proj_dir}/meituan/log')
print(loger)

parser = argparse.ArgumentParser(description="美团组件")
parser.add_argument("-n", "--now", action="store_true", help="今天的数据")
args = parser.parse_args()

if args.now:
    now = datetime.datetime.now()
    now = now - datetime.timedelta(days=1)
    today_midnight = datetime.datetime(now.year, now.month, now.day)
    today_end = today_midnight + datetime.timedelta(hours=23, minutes=59, seconds=59)

    # 转换为 Unix 时间戳（单位：秒）
    begin_timestamp = int(today_midnight.timestamp()*1000)
    end_timestamp = int(today_end.timestamp()*1000)
else:
    begin_timestamp  = env.begin_timestamp_mt
    end_timestamp    = env.end_timestamp_mt


cookies  = env.configjson['cookies']['mt']
proj_dir = env.proj_dir


mt_status = 0

url = "https://e.dianping.com/couponrecord/queryCouponRecordDetails?yodaReady=h5&csecplatform=4&csecversion=3.1.0&mtgsig=%7B%22a1%22%3A%221.2%22%2C%22a2%22%3A1741649588314%2C%22a3%22%3A%221740084568043CAMCCCC2960edaad10e294fa6f28397fe2285903389%22%2C%22a5%22%3A%22Stv5DY8JgwkU6K8t4Du0kW28bQkLXNubi56yxynYvGXmMreHkQD%3D%22%2C%22a6%22%3A%22hs1.6h%2FL%2FxOLbp6kZFEDQEAObwkld84%2FkTqS1g1ljpf6mKulGU6ne9JVuPJdL3LBb3lXNOqAWDnQsCsrrgN1VbGtpQ6KFddNpdWZhbJyHp9BouTHef3eztuAH%2Fr%2Bz8iKD5o8z%22%2C%22a8%22%3A%22d4cec0195eb597922168c13086f2db17%22%2C%22a9%22%3A%223.1.0%2C7%2C77%22%2C%22a10%22%3A%22e4%22%2C%22x0%22%3A4%2C%22d1%22%3A%22f9ac135a402fd1f6a9965235b983c2a0%22%7D"

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


try:
    response = requests.post(url, headers=headers, json=data, cookies=cookies)
    json_data = response.json()

    with open(f"{proj_dir}/meituan/meituan.json",'w') as data_json:
        json.dump(response.json(), data_json, ensure_ascii=False, indent=4)

    sale_price_sum = 0
    if json_data["data"]["couponRecordDetails"]:
        for record in json_data["data"]["couponRecordDetails"]:
            sale_price = record["salePrice"].replace("¥", "")  # 去除货币符号
            sale_price_sum += float(sale_price)
    else:
        sale_price_sum = None

    if sale_price_sum:
        sale_price_sum = round(sale_price_sum, 2) 

except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")
except json.JSONDecodeError:
    print("响应不是有效的JSON")
except Exception as e:
    print(f"发生未知错误：{e}")
    mt_status = 1
    loger.debug('美团出现错误哦')

def get_meituanSum():
    return sale_price_sum

if __name__ == "__main__":
    print(response.json())
    print(get_meituanSum())
