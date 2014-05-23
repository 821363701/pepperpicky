# coding=utf-8
__author__ = 'yuxizhou'

import requests
from BeautifulSoup import BeautifulSoup
import time
from datetime import datetime


session = '?session=4cadd0ed_27729491'
t = 'bid="lOFs30E7sxo"; ll="108296"; __utma=30149280.1960798155.1388989048.1390898784.1391832655.9; __utmz=30149280.1391832655.9.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); mbid=a19de12b; mdbs=295ed83cfb11ebaa7c1c88b6f135c2fe:9a657a1c1255e146:27729491'

###############################################################################

cookies = dict()
cs = t.split(';')
for c in cs:
    parts = c.strip().split('=')
    cookies[parts[0]] = parts[1]


def _search_in_group_topics(list, judge=None, _info=None):
    for item in list:
        link = item.contents[1].attrs[0][1]
        # print link
        # print item.contents[1].text

        hot_url = 'http://m.douban.com'+link

        if judge:
            if judge(hot_url):
                continue

        rr = requests.get(hot_url, cookies=cookies)
        soup = BeautifulSoup(rr.text)
        founder = soup.find('a', {'class': 'founder'})

        content = soup.find('div', {'class': 'entry item'})
        title = content.previous.previous

        # /people/89241363/groups?session=c4338de0_27729491
        # /people/89241363/about?session=0f95d97c_27729491
        founder_url = founder.attrs[0][1].replace('groups', 'about')
        # print founder_url
        # print founder.text

        rrr = requests.get('http://m.douban.com'+founder_url, cookies=cookies)
        soup = BeautifulSoup(rrr.text)
        info = soup.find('div', {'class': 'info'})

        if item.contents[1].text.find(u'上海') > -1 or item.contents[1].text.find(u'魔都') > -1 \
                or -1 < item.contents[1].text.find(u'南京'):
            if _info:
                _info(u'{} {} {} {}'.format(hot_url, u'上海', title, founder_url))
            print u'{} - {}'.format(hot_url.replace('m.', ''), title)
            # webbrowser.open(hot_url.replace('m.', ''))
            continue

        if len(info.contents) > 6:
            if info.contents[6].find(u'上海') > -1:
                if _info:
                    _info(u'{} {} {} {}'.format(hot_url, u'上海', title, founder_url))
                print u'{} - {} - {}'.format(u'上海', hot_url.replace('m.', ''), title)
            elif info.contents[6].find(u'南京') > -1:
                if _info:
                    _info(u'{} {} {} {}'.format(hot_url, u'南京', title, founder_url))
                print u'{} - {} - {}'.format(u'南京', hot_url.replace('m.', ''), title)
            elif info.contents[6].find(u'东营') > -1:
                if _info:
                    _info(u'{} {} {} {}'.format(hot_url, u'东营', title, founder_url))
                print u'{} - {} - {}'.format(u'东营', hot_url.replace('m.', ''), title)
            elif info.contents[6].find(u'六安') > -1:
                if _info:
                    _info(u'{} {} {} {}'.format(hot_url, u'六安', title, founder_url))
                print u'{} - {} - {}'.format(u'六安', hot_url.replace('m.', ''), title)
            else:
                # not shanghai
                pass
                print info.contents[6]
        else:
            # no location
            pass
            # print 'no '


def _get_latest_topic_list():
    url_group = 'http://m.douban.com/group/topics'

    r = requests.get(url_group+session, cookies=cookies)
    soup = BeautifulSoup(r.text)
    return soup.findAll('div', {'class': 'item'})


def get_from_latest_topic():
    l = _get_latest_topic_list()
    _search_in_group_topics(l)


def _get_group_list(gid):
    r = requests.get('http://m.douban.com/group/'+gid+'/'+session, cookies=cookies)
    soup = BeautifulSoup(r.text)
    return soup.findAll('div', {'class': 'item'})


def _get_group_list_139316():
    return _get_group_list('139316')


def _get_group_list_294565():
    return _get_group_list('294565')


def get_from_group(gid):
    l = _get_group_list(gid)
    _search_in_group_topics(l)


def watch_latest(get_list):
    visited = set()
    _info = set()

    try:
        with open('visited', 'r') as fp:
                for l in fp:
                    visited.add(l[:-1])
    except:
        print 'no visited file'

    try:
        with open('info', 'r') as fp:
                for l in fp:
                    _info.add(l[:-1])
    except:
        print 'no info file'

    def judge(u):
        uu = str(u.split('?')[0])
        if uu not in visited:
            visited.add(uu)
            return False
        else:
            return True

    def info(l):
        _info.add(l)

    while True:
        list = get_list()

        _search_in_group_topics(list, judge, info)

        fp = open('visited', 'w')
        for l in visited:
            fp.write(l+'\n')
        fp.close()

        fp = open('info', 'w')
        for l in _info:
            try:
                fp.write(l.encode('utf8'))
                fp.write('\n')
            except:
                fp.write(l)
                fp.write('\n')
        fp.close()

        time.sleep(30)
        print str(len(visited))+'-----------------------------------------------------------'+datetime.now().strftime('%Y%m%d %H:%M:%S')

if __name__ == '__main__':
    # get_from_group('294565')
    # get_from_group('139316')
    # get_from_latest_topic()

    watch_latest(_get_latest_topic_list)
    # watch_latest(_get_group_list_294565)