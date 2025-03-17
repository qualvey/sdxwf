
from urllib.parse import urlencode,urlunparse
from datetime import datetime, timedelta
from tools import env, iheader
import requests
from worktime import get_userid
import json

def get_previous_week_range(dt):
    # 计算当前日期是星期几，星期一为0，星期日为6
    current_weekday = dt.weekday()
    # 计算上周日距离当前日期的天数
    days_since_last_sunday = current_weekday + 1
    # 计算上周日的日期
    last_sunday = dt - timedelta(days=days_since_last_sunday)
    # 计算上周一的日期
    last_monday = last_sunday - timedelta(days=6)
    week_dates = [last_monday + timedelta(days=i) for i in range(7)]
    return week_dates

#obj_mon, obj_sun = get_previous_week_range(env.work_datetime)
#mon = str(obj_mon)
#sun = str(obj_sun)


scheme = 'https'
netloc = 'hub.sdxnetcafe.com'
path = '/api/admin/work/attendance/list'

params =''
# 查询参数

fragment = ''

def get_total_duration(data_json):

    duration_sum = 0
    data_json['data']['total'] == 7
    data_list = data_json['data']['rows'] 

    for item in data_list:
        duration_sum += item['duration']
    return duration_sum

def  write_to_file(response_data):
    try:
        new_data = response_data.json()
        duration = get_total_duration(new_data)
        file_path="./worktime.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    # 如果文件为空或内容不是有效的 JSON，初始化为空列表
                        data = []
        except FileNotFoundError:
            data = []
        if isinstance(data, list):
            # 将新数据追加到列表中
            data.append(new_data)
        else:
            # 如果数据不是列表，可能是字典或其他结构，根据需要处理
            print("现有数据不是列表，无法追加新数据。")
            # 视情况决定是将数据转换为列表，还是采取其他措施
            # 例如，将现有数据和新数据放入一个新的列表中
            data = [data, new_data]
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return new_data
    except requests.exceptions.JSONDecodeError:
        print("响应内容不是有效的 JSON 格式")

def request_get(id):
    query = {
        "startTm":  mon,
        "endTm":    sun,
        "page": 1,
        "limit": 10,
        "userId": id,
        "branchId": "a92fd8a33b7811ea87766c92bf5c82be"
    }
    query_string = urlencode(query)
    url = urlunparse((scheme, netloc, path, params, query_string, fragment))
    response  = requests.get(url, headers=iheader.headers)
    return response.json()
    #if response.ok:
    #    write_to_file(response)
    #else:
    #    print(f"请求失败，状态码：{response.status_code}")

durations = {}
def duration_everyone():
    for name, id in get_userid.userIDs.items():
        data_json =  request_get(id)
        duration_of_name = get_total_duration(data_json)
        durations[name] = duration_of_name 

duration_everyone()

print(durations)
