# coding=utf-8
__author__ = 'yu'

import signal
import sys
import datetime
from pymongo import MongoClient
import pymongo
from bson import ObjectId
import requests
from BeautifulSoup import BeautifulSoup, NavigableString
from print_image import image_to_display
from io import BytesIO

c = MongoClient('121.199.5.143').pick
last = None
last_img = []

raw_cookie = 'bid="AVRekjtmmtM"; ue="doubanxiong@live.cn"; ll="108296"; JSESSIONID=aaaELGO44yuImfnEUlb9u; _ga=GA1.2.984907948.1427943741; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1440496720%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dzyk9sQSdhV1nHB1NAGgBOok_elpLXCqwTB1XeMj5yZxoy32UfgMfio2Uy6jpG1Kt-7ZHoHY0mjnrpMVp1nscXK%26wd%3D%26eqid%3Dccf418b800007a4c0000000255bb24e4%22%5D; __utmt=1; dbcl2="27729491:nXHIH9y11JA"; ck="Tmdb"; push_noty_num=2; push_doumail_num=0; _pk_id.100001.8cb4=63415abb32a1a2b2.1427943740.13.1440496732.1440493946.; _pk_ses.100001.8cb4=*; __utma=30149280.984907948.1427943741.1440491295.1440496721.15; __utmb=30149280.3.10.1440496721; __utmc=30149280; __utmz=30149280.1438328054.13.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.2772'
cookies = {}
for coo in raw_cookie.split(';'):
    try:
        d = coo.strip()
        key, value = d.split('=')
        cookies[key] = value
    except:
        pass


def print_beautiful(content):
    for item in content.contents:
        if type(item) == NavigableString:
            if item != '\n':
                print item
            continue

        if item.name == 'img':
            for key, value in item.attrs:
                if key == 'src':
                    print value
                    break

        if item.name == 'br':
            print ''
            continue

        if len(item.contents) > 0:
            print_beautiful(item)


def quit():
    print 'see you :)'
    sys.exit()


def show():
    global last_img
    last_img = []

    for l in c.all_topic.find({
        'keyword': u'上海',
        'read': {
            '$ne': 1
        }
    }, limit=1).sort('_id', pymongo.DESCENDING):
        # l['topic_id'], l['keyword'], l['founder_id'], l['topic_title'], l['timestamp'], str(l['_id'])
        global last
        last = {
            'id': str(l['_id']),
            'topic_id': l['topic_id'],
            'deny_id': l['founder_id']
        }
        print u'{} - {}'.format(l['topic_title'], datetime.datetime.fromtimestamp(float(l['timestamp'])).strftime('%m-%d %H:%M'))


def detail():
    if not last:
        print 'no last topic'
        return

    topic_url = "http://www.douban.com/group/topic/"+last['topic_id']

    r = requests.get(topic_url, cookies=cookies)
    soup = BeautifulSoup(r.text)
    r.close()

    if r.status_code == 404:
        print '404'
        return

    writer = soup.find('span', {'class': 'from'})
    name = writer.find('a').text
    print u'+-------------------------'
    print u'| name: {}'.format(name)
    belong = soup.find('div', {'class': 'title'}).find('a').text
    print u'| belong: {}'.format(belong)
    print u'+-------------------------'

    content = soup.find('div', {'class': 'topic-content'})
    print_beautiful(content)


def deny():
    if not last:
        print 'no last topic'
        return

    c.deny_id.insert({
        'deny_id': last['deny_id']
    })

    c.all_topic.remove({
        'founder_id': last['deny_id']
    })

    show()


def read():
    if not last:
        print 'no last topic'
        return

    c.all_topic.update({
        '_id': ObjectId(last['id'])
    }, {
        '$set': {
            'read': 1
        }
    })

    show()


def img():
    if len(last_img) > 0:
        for i in last_img:
            resp = requests.get(i)
            image_to_display(BytesIO(resp.content))
    else:
        print 'no img :( '


def init():
    ctrl_c_handler = lambda signum, frame: quit()
    signal.signal(signal.SIGINT, ctrl_c_handler)


def listen():
    show()

    while True:
        line = raw_input('[pepper] ')

        if line == 'detail':
            detail()
        elif line == 'deny':
            deny()
        elif line == 'read':
            read()
        elif line == 'img':
            img()
        else:
            print 'not supported command :( '


if __name__ == "__main__":
    init()
    listen()