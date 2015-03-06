# coding=utf-8
__author__ = 'yuxizhou'

import requests
from BeautifulSoup import BeautifulSoup
import time
from datetime import datetime
import webbrowser


key_word = [u'上海', u'魔都', u'南京', u'东营']
target_area = [u'上海', u'江苏南京']
watch_group = ['139316', '294565', '274483', '331631', '258401', '59335', '233931']
session = '?id=27729491&session=d4a63410c4cf668feb8ec8fa73ec95db1c19cefc'
t = 'viewed="6998797"; bid="n49InUGYqvg"; ll="108296"; dp=1; _ga=GA1.2.2098189400.1390826620; __utmt=1; ap=1; ps=y; ue="doubanxiong@live.cn"; dbcl2="27729491:o75dit0+w+g"; ck="6--W"; push_noty_num=0; push_doumail_num=3; __utma=30149280.2098189400.1390826620.1425542831.1425547321.50; __utmb=30149280.24.9.1425547406801; __utmc=30149280; __utmz=30149280.1425542831.49.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.2772; mbid=eb497e49; mdbs=295ed83cfb11ebaa7c1c88b6f135c2fe:9a657a1c1255e146:27729491'


def contain_keyword(content):
    for key in key_word:
        if content.find(key) > -1:
            return True
    return False


def print_open(url, title):
    print u'{} - {}'.format(url, title)
    webbrowser.open(url)


class Picker(object):
    def __init__(self):
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

    def __append_user_area(self, url, area):
        u_url = unicode(url)
        u_area = unicode(area)

        self.user_area[url] = u_area
        with open('user_area', 'a') as fp:
            fp.write(u'{}\t{}\n'.format(u_url, u_area).encode('utf8'))

    def __append_target_info(self, url, area, founder_url, title):
        with open('target_info', 'a') as fp:
            fp.write(u'{}\t{}\t{}\t{}\n'.format(url, area, founder_url, title).encode('utf8'))

    def __append_visited_topic(self, url, title):
        self.visited_topic.add(url)

        with open('visited_topic', 'a') as fp:
            fp.write(u'{}\t{}\n'.format(url, title).encode('utf8'))

    def __search_in_group_topics(self, topics):
        for item in topics:
            # # check if group is target group
            #
            # belong_group = item.contents[3].contents[1].attrs[0][1]
            #
            # belong_group_id = belong_group.split('?')[0][7:-1]
            # if belong_group_id not in watch_group:
            #     continue

            # check if link is visited

            link = item.contents[1].attrs[0][1]
            topic_title = item.contents[1].text

            hot_url = 'http://m.douban.com'+link
            hot_url_unique = hot_url.split('?')[0]

            if hot_url_unique in self.visited_topic:
                continue

            # visit the hot url

            self.__append_visited_topic(hot_url_unique, topic_title)

            rr = requests.get(hot_url, cookies=self.cookies)
            soup = BeautifulSoup(rr.text)

            # check if founder is not target area

            founder = soup.find('a', {'class': 'founder'})
            founder_url = founder.attrs[0][1].replace('groups', 'about')
            founder_url_unique = founder_url.split('?')[0]

            if founder_url_unique in self.user_area and self.user_area[founder_url_unique] not in target_area:
                continue

            # title contain key word

            content = soup.find('div', {'class': 'entry item'})
            title = content.previous.previous

            if contain_keyword(title):
                self.__append_target_info(hot_url_unique, u'上海', founder_url_unique, title)
                print_open(hot_url.replace('m.', ''), title)
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

                self.__append_user_area(founder_url_unique, founder_area)
                print founder_area
            else:
                # no location
                pass
                # print 'no '

    def __get_latest_topic_list(self):
        url_group = 'http://m.douban.com/group/topics'

        r = requests.get(url_group+session, cookies=self.cookies)
        soup = BeautifulSoup(r.text)
        return soup.findAll('div', {'class': 'item'})

    def __get_group_list(self, gid):
        r = requests.get('http://m.douban.com/group/'+gid+'/'+session, cookies=self.cookies)
        soup = BeautifulSoup(r.text)
        return soup.findAll('div', {'class': 'item'})

    def __start(self, get_list):
        while True:
            self.__search_in_group_topics(get_list())

            time.sleep(20)
            print '-----------------------------------------------------------'+datetime.now().strftime('%Y%m%d %H:%M:%S')

    def start_latest(self):
        self.__start(self.__get_latest_topic_list)

    def start_group(self, group_id):
        def get_list():
            return self.__get_group_list(group_id)

        self.__start(get_list)

if __name__ == '__main__':
    p = Picker()
    p.start_latest()