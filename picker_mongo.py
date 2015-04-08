# coding=utf-8
__author__ = 'yuxizhou'

import requests
from BeautifulSoup import BeautifulSoup
import time
from datetime import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
from const import *

logging.basicConfig(filename='picker.log', level=logging.INFO)

session = '?id=27729491&session=d4a63410c4cf668feb8ec8fa73ec95db1c19cefc'
t = 'viewed="6998797"; bid="n49InUGYqvg"; ll="108296"; dp=1; _ga=GA1.2.2098189400.1390826620; __utmt=1; ap=1; ps=y; ue="doubanxiong@live.cn"; dbcl2="27729491:o75dit0+w+g"; ck="6--W"; push_noty_num=0; push_doumail_num=3; __utma=30149280.2098189400.1390826620.1425542831.1425547321.50; __utmb=30149280.24.9.1425547406801; __utmc=30149280; __utmz=30149280.1425542831.49.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.2772; mbid=eb497e49; mdbs=295ed83cfb11ebaa7c1c88b6f135c2fe:9a657a1c1255e146:27729491'


def send_mail(text):
    msg = MIMEText(text)
    msg['Subject'] = 'pepper message'

    msg['From'] = '821363701@qq.com'
    msg['To'] = '821363701@qq.com'

    s = smtplib.SMTP_SSL('smtp.exmail.qq.com')
    s.login('821363701@qq.com', '821363701pepper')
    s.sendmail('821363701@qq.com', ['821363701@qq.com'], msg.as_string())
    s.quit()


class Picker(object):
    def __init__(self):
        self.c = MongoClient('121.199.5.143').pick

        self.check_group = False
        self.sleep_time = 1

        self.cookies = dict()
        cs = t.split(';')
        for cookie in cs:
            parts = cookie.strip().split('=')
            self.cookies[parts[0]] = parts[1]

        self.fetch_last_ts = time.time()

    def __append_all_topic(self, url, area, founder_url, title):
        topic_id = url.split('topic')[1][1:-1]
        founder_id = founder_url[8:-6]

        self.c.all_topic.insert({
            'topic_id': topic_id,
            'topic_title': title,
            'keyword': area,
            'founder_id': founder_id,
            'timestamp': str(time.time()),
            'source': SOURCE_DOUBAN,
        })

    def __append_visited_topic(self, url, title):
        topic_id = url.split('/')[-2]

        self.c.visited_topic.insert({
            'topic_id': topic_id,
            'topic_title': title
        })

    def __fetch(self, url):
        interval = time.time() - self.fetch_last_ts
        if interval < 0.5:
            time.sleep(0.5)

        self.fetch_last_ts = time.time()

        try:
            result = requests.get(url, cookies=self.cookies, timeout=10)
        except:
            result = requests.get(url, cookies=self.cookies)
        return result

    def __search_in_group_topics(self, topics):
        count_total = len(topics)
        count_visited = 0
        count_deny = 0
        count_save = 0

        for item in topics:
            if self.check_group:
                # todo use group to filter
                belong_group = item.contents[3].contents[1].attrs[0][1]
                belong_group_id = belong_group.split('?')[0][7:-1]

            # check if link is visited

            link = item.contents[1].attrs[0][1]
            topic_title = item.contents[1].text

            hot_url = 'http://m.douban.com'+link
            hot_url_unique = hot_url.split('?')[0]

            hot_url_unique_id = hot_url_unique.split('/')[-2]
            visited = self.c.visited_topic.find_one({
                'topic_id': hot_url_unique_id
            })
            if visited:
                count_visited += 1
                continue

            # visit the hot url

            self.__append_visited_topic(hot_url_unique, topic_title)

            rr = self.__fetch(hot_url)
            soup = BeautifulSoup(rr.text)

            # check if founder is denied

            founder = soup.find('a', {'class': 'founder'})
            if not founder:
                # may be the topic is removed
                continue
            founder_url = founder.attrs[0][1].replace('groups', 'about')
            founder_url_unique = founder_url.split('?')[0]

            founder_url_unique_id = founder_url_unique.replace('/about', '')[8:]
            denied = self.c.deny_id.find_one({
                'deny_id': founder_url_unique_id
            })
            if denied:
                count_deny += 1
                continue

            content = soup.find('div', {'class': 'entry item'})
            title = content.previous.previous

            # save the topic

            rrr = self.__fetch('http://m.douban.com'+founder_url)
            soup = BeautifulSoup(rrr.text)
            founder_info = soup.find('div', {'class': 'info'})

            if founder_info and len(founder_info.contents) > 6:
                founder_area = unicode(founder_info.contents[6].strip())
            else:
                # no location
                founder_area = 'None'

            self.__append_all_topic(hot_url_unique, founder_area, founder_url_unique, title)
            count_save += 1

        l = '[total: {} visited: -{} deny: -{}] = [save: {}] - {}'.format(
            count_total, count_visited, count_deny, count_save, datetime.now().strftime('%Y%m%d %H:%M:%S'))
        print l
        logging.info(l)

    def __get_latest_topic_list(self):
        result = []
        for i in range(1, 4):
            url_group = 'http://m.douban.com/group/topics'

            r = self.__fetch(url_group + session + '&page=' + str(i))
            soup = BeautifulSoup(r.text)
            result.extend(soup.findAll('div', {'class': 'item'}))
        return result

    def __get_group_list(self, gid):
        r = self.__fetch('http://m.douban.com/group/'+gid+'/'+session)
        soup = BeautifulSoup(r.text)
        return soup.findAll('div', {'class': 'item'})

    def __start(self, get_list):
        while True:
            try:
                self.__search_in_group_topics(get_list())
            except Exception, e:
                logging.error(e)

    def start_latest(self):
        self.sleep_time = 10
        self.check_group = False

        self.__start(self.__get_latest_topic_list)

    def start_group(self, group_id):
        self.check_group = False
        self.sleep_time = 5

        def get_list():
            return self.__get_group_list(group_id)

        self.__start(get_list)

    def start_ex(self):
        self.sleep_time = 1
        self.check_group = False

        while True:
            try:
                self.__search_in_group_topics(self.__get_latest_topic_list())
                # self.__search_in_group_topics(self.__get_group_list('516876'))
            except Exception, e:
                logging.error(e)
                send_mail(str(e))

    def fetch(self, url):
        return self.__fetch(url)

if __name__ == '__main__':
    p = Picker()
    p.start_ex()

    # p.start_latest()
    # p.start_group('139316')
