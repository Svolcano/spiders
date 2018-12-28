import requests
import random
from lxml import etree

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/601.1.10 (KHTML, like Gecko) Version/8.0.5 Safari/601.1.10",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; ; NCT50_AAP285C84A1328) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"
]
base = 'https://mbasic.facebook.com'
user_agent = random.choice(USER_AGENTS)
header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': base,
    'Origin': base,
    'User-Agent': user_agent,
    'Connection': 'keep-alive',
}

s = requests.Session()
now_cookies = s.cookies
now_cookies.clear()
resp = s.get(base, headers=header)
login_url = 'https://mbasic.facebook.com/login/device-based/regular/login/?refsrc=https://mbasic.facebook.com/&lwv=100&refid=8'
dom = etree.HTML(resp.content)
inputs = dom.xpath("//form//input")
login_params = {}
for i in inputs:
    k = i.get('name')
    v = i.get('value')
    login_params[k] = v
login_params['try_number'] = 0
login_params['email'] = '18332537701'
login_params['pass'] = '19931103SJYA'
login_params['login'] = 'Log In'
resp = s.post(login_url, data=login_params)

if "Log In With One Tap" in resp.text:
    relogin_url = 'https://mbasic.facebook.com/login/device-based/update-nonce/'
    relogin_param = {}
    dom = etree.HTML(resp.content)
    inputs = dom.xpath("//form/input")
    for i in inputs:
        k = i.get('name')
        v = i.get('value', '')
        relogin_param[k] = v
    resp = s.post(relogin_url, data=relogin_param)

home_url = 'https://mbasic.facebook.com/home.php?_rdr'
resp = s.get(home_url)

post_params = {}
dom = etree.HTML(resp.content)
inputs = dom.xpath("//form/input")
for i in inputs:
    k = i.get('name')
    v = i.get('value', '')
    post_params[k] = v
post_suffix = dom.xpath('//form[@method="post"]/@action')[0]
post_url = f"{base}{post_suffix}"
post_params['view_post'] = 'Post'
post_params['xc_message'] = 'good good study, day day up!'
resp = s.post(post_url, data=post_params)
with open("aa.html", 'w', encoding='utf-8') as wh:
    wh.write(resp.text)
print('done')