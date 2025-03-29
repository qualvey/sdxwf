import meituan.main as mt
import douyin.main as dy
from datetime import date

# 获取今天的日期
today = date.today()
print("今天的日期:", today)

douyin_sum = dy.get_douyinSum(today)
meituan_sum = mt.get_meituanSum(today)

print(douyin_sum)
print(meituan_sum)
print(douyin_sum+meituan_sum)
