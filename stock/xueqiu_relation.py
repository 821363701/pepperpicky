__author__ = 'yuxizhou'

import requests
import json
from pymongo import MongoClient

c = MongoClient('121.199.5.143').xueqiu
c.user.ensure_index('xueqiu_id')
c.user.ensure_index('crawl')
c.relation.ensure_index('from')
c.relation.ensure_index('to')


t = 's=o7t11psumz; bid=48b811c1fb337a55d9ab1c6e71e55c9a_ifuy3jz5; snbim_minify=true; xq_a_token=92ea46c780bc39aef205076edffc3a49775d1de4; xq_r_token=4104f33493625c0724051c7e69252c738809ad54; u=5835289916; xq_token_expire=Tue%20Nov%2017%202015%2021%3A47%3A54%20GMT%2B0800%20(CST); xq_is_login=1; __utmt=1; __utma=1.538315531.1425537834.1445355685.1445606212.4; __utmb=1.11.10.1445606212; __utmc=1; __utmz=1.1445077956.2.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1445077956,1445355685,1445606212; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1445608079'
cookies = dict()
cs = t.split(';')
for cookie in cs:
    parts = cookie.strip().split('=')
    cookies[parts[0]] = parts[1]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
}


url_node = 'http://xueqiu.com/friendships/groups/members.json?page={}&uid={}&gid=0&_=1445608085800'
start_node = 1538598451
start = c.user.find_one({
    'xueqiu_id': start_node
})
if not start:
    c.user.insert({
        'xueqiu_id': start_node,
        'crawl': 0
    })


def get_cares(node_id):
    page = 1
    max_page = 1
    care = []
    while page <= max_page:
        url = url_node.format(page, node_id)
        r = requests.get(url, cookies=cookies, headers=headers)
        result = json.loads(r.text)

        page = result['page']
        max_page = result['maxPage']
        for user in result['users']:
            care.append(user['id'])
        page += 1
        r.close()
        # time.sleep(1)
    return care


def do_job(job):
    cares = get_cares(job)
    print '{} {}'.format(job, len(cares))
    for care in cares:
        c.relation.update({
            'from': job,
            'to': care
        }, {
            'from': job,
            'to': care
        }, True)

        one = c.user.find_one({
            'xueqiu_id': care
        })
        if not one:
            c.user.insert({
                'xueqiu_id': care,
                'crawl': 0
            })


while True:
    one = c.user.find_one({
        'crawl': 0
    })
    if one:
        do_job(one['xueqiu_id'])

        c.user.update({
            'xueqiu_id': one['xueqiu_id']
        }, {
            '$set': {
                'crawl': 1
            }
        })
    else:
        print 'all job done'