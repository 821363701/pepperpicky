__author__ = 'yu'

import requests

t = 's=9h51vwkpf3; xq_a_token=a5bca17a95dd0db35b246aefef70b2826122e894; xqat=a5bca17a95dd0db35b246aefef70b2826122e894; xq_r_token=844b78d28532416b563d777f3835d6f1683a47cf; xq_is_login=1; u=5835289916; xq_token_expire=Fri%20Sep%2025%202015%2012%3A11%3A28%20GMT%2B0800%20(CST); bid=48b811c1fb337a55d9ab1c6e71e55c9a_idzeslpr; snbim_minify=true; __utmt=1; __utma=1.1788090167.1439260364.1440999220.1442197483.4; __utmb=1.2.10.1442197483; __utmc=1; __utmz=1.1439260364.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E9%9B%AA%E7%90%83; Hm_lvt_1db88642e346389874251b5a1eded6e3=1440994250; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1442197486'

cookies = dict()
cs = t.split(';')
for cookie in cs:
    parts = cookie.strip().split('=')
    cookies[parts[0]] = parts[1]

target = 'http://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH010389'


r = requests.get(target, cookies=cookies, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
})

print r.status_code
print r.text