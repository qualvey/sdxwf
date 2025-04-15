import requests
import json
import datetime
import pytz
from openpyxl.styles    import Font
from openpyxl.cell.text import InlineFont 
from openpyxl.cell.rich_text import TextBlock, CellRichText

from http.cookies import SimpleCookie
from tools    import env
from tools.iheader import headers

scheme = 'https://'
hostname = headers['Host']

def fetch_specialFee(datetime_obj):
    date_str = datetime_obj.strftime('%Y-%m-%d')
    api_path = '/api/payment/order/specialFree/list'
    params   = {
        'orderNo': '',
        'page'  : 1,
        'limit' : 100,
        'sortName': 'submitAt',
        'sortOrder': 'desc',
        'branchId' : 'a92fd8a33b7811ea87766c92bf5c82be',
        'startTm'  : f'{date_str} 00:00:00',
        'endTm'    : f'{date_str} 23:59:59'
    }
    url = f"{scheme}{hostname}{api_path}"
    response = requests.get(url,params = params,  headers=headers)
    data     = response.json()
    with open(f"{env.proj_dir}/specialFee/special.json", "w", encoding="UTF-8") as cache:
        json.dump(data, cache, ensure_ascii=False, indent=4)
    return data

def resolve_data(data_json):
    special_reason_totals = {}
    for item in data_json['data']['rows']:
        if item['status']=='COMPLETED':
        #status有可能是其他状态，比如 "CANCELLED"
            reason = item['specialReason']
            amount = float(item['totalAmount'])  # 将金额转换为浮点数
            amount_int = int(amount)
            if '红包' in reason:
                continue
            if "吃鸡" in reason or '游戏' in reason:
                reason = "游戏奖励"
            # 如果 specialReason 已在字典中，累加金额；否则，初始化为当前金额
            if reason in special_reason_totals:
                special_reason_totals[reason] += amount_int
            else:
                special_reason_totals[reason] = amount_int
    #breakpoint()
    return special_reason_totals

def format_specialFee(data, special_code, reverse=False):

    #用dict数据结构来存储
    speciallist = []
    if special_code:
        return None
    else:
        # 根据 reverse 参数决定排序顺序
        sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=reverse)
        # 计算 reason 字段的最大长度
        max_reason_length = max(len(reason) for reason, _ in sorted_items)

        for index, (reason, total) in enumerate(sorted_items, start=1):
            
            padding_length = (max_reason_length - len(reason)) * 3

            item = f"{index}. {reason:<{max_reason_length + padding_length}}：{total}"
            speciallist.append(item)
        return speciallist

def get_specialFee(datetime_obj):
    fee_data = fetch_specialFee(datetime_obj)
    data_section = fee_data.get('data')
    special_code = None
    if data_section:
        rows = data_section.get('rows')
        if rows:
            special_code = 0
            special_reason_totals = resolve_data(fee_data)
        else:
            special_code = 1
            print("specialFee error")
    else:
        special_code = 1
        print("specialFee error")
    sum  = 0 
    for (name, value) in special_reason_totals.items():
        sum += value

    speciallist = format_specialFee(special_reason_totals,special_code)

    return speciallist, sum

