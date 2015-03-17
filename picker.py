# coding=utf-8
__author__ = 'yuxizhou'

import requests
from BeautifulSoup import BeautifulSoup
import time
from datetime import datetime
import webbrowser
import logging

logging.basicConfig(filename='picker.log', level=logging.INFO)

key_word = [u'上海', u'魔都', u'南京', u'东营', u'征']
target_area = [u'上海', u'江苏南京']
watch_group = ['139316', '294565', '274483', '331631', '258401', '59335', '233931']
session = '?id=27729491&session=d4a63410c4cf668feb8ec8fa73ec95db1c19cefc'
t = 'viewed="6998797"; bid="n49InUGYqvg"; ll="108296"; dp=1; _ga=GA1.2.2098189400.1390826620; __utmt=1; ap=1; ps=y; ue="doubanxiong@live.cn"; dbcl2="27729491:o75dit0+w+g"; ck="6--W"; push_noty_num=0; push_doumail_num=3; __utma=30149280.2098189400.1390826620.1425542831.1425547321.50; __utmb=30149280.24.9.1425547406801; __utmc=30149280; __utmz=30149280.1425542831.49.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.2772; mbid=eb497e49; mdbs=295ed83cfb11ebaa7c1c88b6f135c2fe:9a657a1c1255e146:27729491'


def contain_keyword(content):
    for key in key_word:
        if content.find(key) > -1:
            return key
    return None


def print_open(url, title):
    print u'{} - {}'.format(url, title)
    # webbrowser.open(url)


class Picker(object):
    def __init__(self):
        self.check_group = True
        self.sleep_time = 10

        self.deny_id = set()
        self.visited_topic = set()
        self.user_area = dict()

        self.cookies = dict()
        cs = t.split(';')
        for c in cs:
            parts = c.strip().split('=')
            self.cookies[parts[0]] = parts[1]

        self.__load_config()

    def __load_config(self):
        # visited_topic

        try:
            with open('visited_topic', 'r') as fp:
                for l in fp:
                    ll = l[:-1].split('\t')
                    self.visited_topic.add(ll[0])
        except IOError:
            print 'no visited_topic file'

        # user_area

        try:
            with open('user_area', 'r') as fp:
                for l in fp:
                    ll = l[:-1].split('\t')
                    self.user_area[ll[0]] = ll[1].decode('utf8')
        except IOError:
            print 'no user_area file'

    def __period_load_config(self):
        # deny_id

        try:
            with open('deny_id', 'r') as fp:
                for l in fp:
                    self.deny_id.add(l[:-1])
        except IOError:
            print 'no deny_id file'

    def __append_user_area(self, url, area):
        u_url = unicode(url)
        u_area = unicode(area)

        self.user_area[url] = u_area
        with open('user_area', 'a') as fp:
            fp.write(u'{}\t{}\n'.format(u_url, u_area).encode('utf8'))

    def __append_target_info(self, url, area, founder_url, title):
        with open('target_info', 'a') as fp:
            fp.write(u'{}\t{}\t{}\t{}\t{}\n'.format(url, area, founder_url, title, str(time.time())).encode('utf8'))

    def __append_visited_topic(self, url, title):
        self.visited_topic.add(url)

        with open('visited_topic', 'a') as fp:
            fp.write(u'{}\t{}\n'.format(url, title).encode('utf8'))

    def __search_in_group_topics(self, topics):
        count_total = len(topics)
        count_group = 0
        count_visited = 0
        count_not_target_area_before = 0
        count_not_target_area = 0
        count_deny = 0
        count_keyword_open = 0
        count_target_area = 0

        for item in topics:
            if self.check_group:
                # check if group is target group

                belong_group = item.contents[3].contents[1].attrs[0][1]

                belong_group_id = belong_group.split('?')[0][7:-1]
                if belong_group_id not in watch_group:
                    count_group += 1
                    continue

            # check if link is visited

            link = item.contents[1].attrs[0][1]
            topic_title = item.contents[1].text

            hot_url = 'http://m.douban.com'+link
            hot_url_unique = hot_url.split('?')[0]

            if hot_url_unique in self.visited_topic:
                count_visited += 1
                continue

            # visit the hot url

            self.__append_visited_topic(hot_url_unique, topic_title)

            rr = requests.get(hot_url, cookies=self.cookies)
            soup = BeautifulSoup(rr.text)

            # check if founder is not target area

            founder = soup.find('a', {'class': 'founder'})
            founder_url = founder.attrs[0][1].replace('groups', 'about')
            founder_url_unique = founder_url.split('?')[0]

            if founder_url_unique.replace('/about', '')[8:-1] in self.deny_id:
                count_deny += 1
                continue

            if founder_url_unique in self.user_area and self.user_area[founder_url_unique] not in target_area:
                count_not_target_area_before += 1
                continue

            # title contain key word

            content = soup.find('div', {'class': 'entry item'})
            title = content.previous.previous

            title_keyword = contain_keyword(title)
            if title_keyword:
                self.__append_target_info(hot_url_unique, title_keyword, founder_url_unique, title)
                print_open(hot_url.replace('m.', ''), title)
                count_keyword_open += 1
                continue

            # check if user is in target area

            rrr = requests.get('http://m.douban.com'+founder_url, cookies=self.cookies)
            soup = BeautifulSoup(rrr.text)
            founder_info = soup.find('div', {'class': 'info'})

            if founder_info and len(founder_info.contents) > 6:
                founder_area = unicode(founder_info.contents[6].strip())

                if founder_area in target_area:
                    self.__append_target_info(hot_url_unique, founder_area, founder_url_unique, title)
                    print_open(hot_url.replace('m.', ''), title)
                    count_target_area += 1
                else:
                    count_not_target_area += 1

                self.__append_user_area(founder_url_unique, founder_area)
            else:
                # no location
                count_not_target_area += 1
                self.__append_user_area(founder_url_unique, u'None')

        l = '[total: {} group: -{} visited: -{} area: -{} areab: -{} deny: -{}] = [keyword: {} area: {}] - {}'.format(
            count_total, count_group, count_visited, count_not_target_area, count_not_target_area_before, count_deny,
            count_keyword_open, count_target_area, datetime.now().strftime('%Y%m%d %H:%M:%S'))
        print l
        logging.info(l)

    def __get_latest_topic_list(self):
        result = []
        for i in range(1, 5):
            url_group = 'http://m.douban.com/group/topics'

            r = requests.get(url_group+session+'&page='+str(i), cookies=self.cookies)
            soup = BeautifulSoup(r.text)
            result.extend(soup.findAll('div', {'class': 'item'}))
        return result

    def __get_group_list(self, gid):
        r = requests.get('http://m.douban.com/group/'+gid+'/'+session, cookies=self.cookies)
        soup = BeautifulSoup(r.text)
        return soup.findAll('div', {'class': 'item'})

    def __start(self, get_list):
        while True:
            try:
                self.__search_in_group_topics(get_list())
            except Exception, e:
                logging.error(e)
            time.sleep(self.sleep_time)

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
        self.sleep_time = 5
        self.check_group = False

        while True:
            self.__period_load_config()
            try:
                self.__search_in_group_topics(self.__get_latest_topic_list())
                #self.__search_in_group_topics(self.__get_group_list('516876'))
            except Exception, e:
                logging.error(e)
            time.sleep(self.sleep_time)

if __name__ == '__main__':
    p = Picker()
    p.start_ex()
    # p.start_latest()
    # p.start_group('139316')
