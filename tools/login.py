
from io import StringIO
from tools import env
from PIL import Image
from io import BytesIO
import xml.etree.ElementTree as ET

import re
import requests
import json
import time
from tools.iheader import header_launcher

raw_request_get_id = ''' GET /connect/qrconnect?appid=wx5322e698d6ac98d4&scope=snsapi_login&redirect_uri=http%3A%2F%2Fsso.cloudnetcafe.com%2F%23%2FbindingAccount&state=25750&login_type=jssdk&self_redirect=false&styletype=&sizetype=&bgcolor=&rst=&style=black&href=https://hub.sdxnetcafe.com/src/static/wxlogin.css&f=xml&1743032985484&_=1743032647062 HTTP/2
Host: open.weixin.qq.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: application/xml, text/xml, */*; q=0.01
Accept-Language: zh,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br, zstd
X-Requested-With: XMLHttpRequest
Connection: keep-alive
Referer: https://open.weixin.qq.com/connect/qrconnect?appid=wx5322e698d6ac98d4&scope=snsapi_login&redirect_uri=http%3A%2F%2Fsso.cloudnetcafe.com%2F%23%2FbindingAccount&state=25750&login_type=jssdk&self_redirect=false&styletype=&sizetype=&bgcolor=&rst=&style=black&href=https://hub.sdxnetcafe.com/src/static/wxlogin.css
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
'''


def fetch_data(headers):
    '''
    headers:<dict>
    '''
    url = f"https://{headers['Host']}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200: 
        with open(f'{env.proj_dir}/index.html', "wb") as index:
            index.write(response.content)
    return response

def parse_raw_request(raw_request):
    # 使用 StringIO 将原始请求字符串转换为文件对象，方便逐行读取
    request_file = StringIO(raw_request)
    # 读取请求行（例如：GET /connect/qrcode/061p2Za447CUkl2X HTTP/2）
    request_line = request_file.readline().strip()
    # 使用正则表达式解析请求行
    match = re.match(r'(\S+) (\S+) (\S+)', request_line)
    if match:
        method, path, _ = match.groups()
    else:
        raise ValueError("无法解析请求行")
    # 读取头部信息并构建 headers 字典
    headers = {}
    for line in request_file:
        print(line)
        line = line.strip()
        if not line:
            break  # 空行表示头部结束
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    return method, path, headers

def send_raw_request(raw_request):
    method, path, headers = parse_raw_request(raw_request)
    # 构建完整的 URL
    #url = f'https://open.weixin.qq.com{path}'
    url = f'http://{headers['Host']}{path}'

    # 发送请求
    response = requests.request(method, url, headers=headers)
    return response

# 示例用法
#raw_request = '''GET /connect/qrcode/061p2Za447CUkl2X HTTP/2
#Host: open.weixin.qq.com
#User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
#Accept: image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5
#Accept-Language: zh,en-US;q=0.7,en;q=0.3
#Accept-Encoding: gzip, deflate, br, zstd
#Connection: keep-alive
#Referer: https://open.weixin.qq.com/connect/qrconnect?appid=wx5322e698d6ac98d4&scope=snsapi_login&redirect_uri=http%3A%2F%2Fsso.cloudnetcafe.com%2F%23%2FbindingAccount&state=91088&login_type=jssdk&self_redirect=false&styletype=&sizetype=&bgcolor=&rst=&style=black&href=https://hub.sdxnetcafe.com/src/static/wxlogin.css
#Sec-Fetch-Dest: image
#Sec-Fetch-Mode: no-cors
#Sec-Fetch-Site: same-origin
#Priority: u=5, i
#TE: trailers
#'''

#response = send_raw_request(raw_request)

response = send_raw_request(raw_request_get_id)
xml_data = response.text
root = ET.fromstring(xml_data)

# 提取 uuid 的值
uuid = root.find('uuid').text
if not uuid:
    prit('uuid error~!!')
#获取二维码
raw_request_qrcode = f''' GET /connect/qrcode/{uuid} HTTP/2
Host: open.weixin.qq.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5
Accept-Language: zh,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
Referer: https://open.weixin.qq.com/connect/qrconnect?appid=wx5322e698d6ac98d4&scope=snsapi_login&redirect_uri=http%3A%2F%2Fsso.cloudnetcafe.com%2F%23%2FbindingAccount&state=62245&login_type=jssdk&self_redirect=false&styletype=&sizetype=&bgcolor=&rst=&style=black&href=https://hub.sdxnetcafe.com/src/static/wxlogin.css
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
Priority: u=5, i
TE: trailers'''

response_qrcode = send_raw_request(raw_request_qrcode)
def show_img(response_qrcode):
    image = Image.open(BytesIO(response_qrcode.content))
        # 显示图片
    image.show()

show_img(response_qrcode)


#获取wx_code
#要解决的问题：时间戳从哪来

#响应载荷格式：window.wx_errcode=405;window.wx_code='011H1G000wIeYT1NwR300yrNXp2H1G0W';
def lp_wxcode(uuid, max_attempts=10, interval=1):

    for attempt in range(max_attempts):
        timestamp_ms = int(time.time() * 1000)

        raw_request_wxcode = f'''GET /connect/l/qrconnect?uuid={uuid}&last=404&_={timestamp_ms} HTTP/1.1
        Host: lp.open.weixin.qq.com
        User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
        Accept: */*
        Accept-Language: zh,en-US;q=0.7,en;q=0.3
        Accept-Encoding: gzip, deflate, br, zstd
        Connection: keep-alive
        Referer: https://open.weixin.qq.com/
        Sec-Fetch-Dest: script
        Sec-Fetch-Mode: no-cors
        Sec-Fetch-Site: same-site'''
#        params = {
#            "uuid": uuid,
#            "last": "404",
#            "_": timestamp_ms
#        }
        response = send_raw_request(raw_request_wxcode)
        if response.status_code == 200:
                    errcode_match = re.search(r"window\.wx_errcode=(\d+);", response.text)
                    code_match = re.search(r"window\.wx_code='(.*?)';", response.text)
                    if errcode_match:
                        errcode = int(errcode_match.group(1))
                        if errcode == 405 and code_match:
                            wx_code = code_match.group(1)
                            print(f"获取到 wx_code: {wx_code}")
                            return wx_code

        time.sleep(interval)
wx_code = lp_wxcode(uuid=uuid)
print('wx_code', wx_code)

def get_wxcode(response_payload):
    print("---- 处理数据 ----")
    print(response_payload)  # 打印原始数据，看看是不是多次调用了
    match = re.search(r"window\.wx_code='(.*?)';", response_payload)
    if match:
        wx_code = match.group(1)
        print(wx_code)  # 输出: 011H1G000wIeYT1NwR300yrNXp2H1G0W
        return wx_code
    else:
        print("未找到 wx_code")


raw_request_token = f'''POST /api/admin/user/wechatLogin?code={wx_code} HTTP/1.1
Host: sso.cloudnetcafe.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: application/json, text/plain, */*
Accept-Language: zh,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Authorization: null
Origin: http://sso.cloudnetcafe.com
Connection: keep-alive
Referer: http://sso.cloudnetcafe.com/
Content-Length: 0'''

response_token = send_raw_request(raw_request_token)
token = response_token.json()['data']

#至此，token成功获取

