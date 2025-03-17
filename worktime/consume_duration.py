
from tools import iheader, env
from datetime import timedelta
import urllib.parse
import requests
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
date_list = get_previous_week_range(env.work_datetime)

#obj_mon, obj_sun = get_previous_week_range(env.work_datetime)
#mon = str(obj_mon)
#sun = str(obj_sun)

def request_get(date_str):

    url_dict = {
    "scheme": "https",
    "host": "hub.sdxnetcafe.com",
    "filename": "/api/statistics/branch/operation/data/info",
    "query": {
        "branchId": "a92fd8a33b7811ea87766c92bf5c82be",
        "startTm": date_str
        }
    }

    scheme = url_dict.get("scheme", "")
    host = url_dict.get("host", "")
    filename = url_dict.get("filename", "")
    query = url_dict.get("query", {})
    query_string = urllib.parse.urlencode(query)
    url = urllib.parse.urlunparse((scheme, host, filename, '', query_string, ''))
    response  = requests.get(url, headers=iheader.headers)
    return response.json()


duration = 0
for date_items in date_list:
    date_str = str(date_items)
    data     = request_get(date_str)
    duration += data['data']['duration']
print(duration/60)



with open(f"{env.proj_dir}/worktime/data.info.json", 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
