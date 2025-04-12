import requests
import json
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
import pytz
import argparse

import time
from tools import env
from tools.logger import get_logger

logger = get_logger('DOUYIN')



cookie          = env.configjson['cookies']['dy']
url = "https://life.douyin.com/life/trade_view/v1/verify/verify_record_list/?page_index=1&page_size=20&industry=industry_common&root_life_account_id=7136075595087087628"

#def parse_cookie_string(cookie_string):
#    cookie = SimpleCookie()
#    cookie.load(cookie_string)
#    return {key: morsel.value for key, morsel in cookie.items()}

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/json",
        "Agw-Js-Conv": "str",
        "x-tt-ls-session-id": "3d8a7490-f59b-45f0-88c3-a29377e622f9",
        "x-tt-trace-log": "01",
        "x-tt-trace-id": "00-833c459518ddb35cb728491cb-833c459518ddb35c-01",
        "Ac-Tag": "smb_s",
        "rpc-persist-life-merchant-role": "26988990",
        "rpc-persist-life-merchant-switch-role": "1",
        "rpc-persist-life-biz-view-id": "0",
        "rpc-persist-lite-app-id": "100281",
        "rpc-persist-life-platform": "pc",
        "rpc-persist-terminal-type": "1",
        "rpc-persist-session-id": "100281ca-19cf-41b1-a354-8602cbba9e39",
        "x-secsdk-csrf-token": "0001000000016d38742d8b955978119e3da361617a9becfd31c6b5e77b1a15acae6d93c68e85182ba1b38faa45cc",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0"
    }
#cookies = parse_cookie_string(cookie)

def get_douyin_data(date,max_retries=5, delay=2):

    today_start = datetime(date.year, date.month, date.day)
    today_end = today_start + timedelta(hours=23, minutes=59, seconds=59)

    print('抖音数据日期:', today_start,'-',today_end)
    # 转换为 Unix 时间戳（单位：秒）
    begin_timestamp = int(today_start.timestamp())
    end_timestamp = int(today_end.timestamp())

    post_data = {
        "filter":{
            "start_time": begin_timestamp,
            "end_time": end_timestamp,
            "poi_id_list":[],
            "sku_id_list":[],
            "product_option":[],
            "is_market":False,
            "is_market_poi":False
        },
        "is_user_poi_filter":False,
        "is_expend_to_poi":True,
        "auth_poi_extra_filter":{},
        "industry":"industry_common",
        "permission_common_param":{}
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=post_data, headers=headers, cookies=cookie)
            response.raise_for_status()  # 如果状态码不是 200，抛出异常
            json_data = response.json()
            logger.debug("抖音响应 JSON 数据成功")

            with open("douyin.json", 'w', encoding='utf-8') as data_json:
                json.dump(json_data, data_json, ensure_ascii=False, indent=4)

            return json_data  # 请求成功，返回 JSON 数据
        
        except requests.exceptions.RequestException as e:
            logger.error(f"请求发生错误（第 {attempt+1} 次尝试）：{e}")

            if attempt < max_retries - 1:  # 如果还有重试机会，等待后重试
                time.sleep(delay)  # 等待 delay 秒后重试
            else:
                logger.error("已达到最大重试次数，放弃请求")
                return None  # 所有尝试都失败，返回 None


def get_douyinSum(date):
    sum = 0
    json_data = get_douyin_data(date)

    with open("douyin.json", 'w', encoding='utf-8') as data_json:
        json.dump(json_data, data_json, ensure_ascii=False, indent=4)
    try:
        for item in json_data['data']['list']:
            #actual_amount = item['sku']['amount']['actual_amount']
            verify_amount = item['amount']['verify_amount']
            print(verify_amount)
            sum += verify_amount/100
    except:
        pass
    if sum==0:
        return None
    return sum



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="抖音模块")
    parser.add_argument("-n", "--now", action="store_true", help="启用调试模式")
    args = parser.parse_args()
    sum =    get_douyinSum(datetime.today())

    print("总金额",sum)

