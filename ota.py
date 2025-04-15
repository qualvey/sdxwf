import meituan.main as mt
import douyin.main as dy
from datetime import date, datetime, timedelta
#from operation.main import today_income
from operation import ThirdParty
import schedule
import time
from tools.logger import get_logger

logger =  get_logger(__name__)
# 获取今天的日期
today = date.today()
today_datetime=datetime.combine(today, datetime.min.time())
print("今天的日期:", today)

douyin_sum = dy.get_douyinSum(today)
meituan_sum = mt.get_meituanSum(today)
#income = today_income(today)

ota_update  = ThirdParty.ota_update
delete_third = ThirdParty.delete
check_unique = ThirdParty.check_unique

def main():
    logger.warning('updating ota infomation')
    ids = check_unique(today_datetime.strftime('%Y-%m-%d'))
    print(ids)
    for id in ids:
        delete_status = delete_third(id)

    ota_update(ota_name='MEITUAN', date_obj=today_datetime, income=meituan_sum)
    ota_update(ota_name='DOUYIN', date_obj=today_datetime, income=douyin_sum)

main()
schedule.every(30).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
#
#
print(f'抖音收入{douyin_sum}')
print(f'美团收入{meituan_sum}')
#print(f'收银台收入{income}')
print(f'总ota收入{douyin_sum+meituan_sum}')
#
#def web_entry():
#    return income
#
