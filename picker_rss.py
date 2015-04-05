# coding=utf-8
__author__ = 'yuxizhou'

import feedparser

python_wiki_rss_url = "http://www.douban.com/feed/group/kaopulove/discussion"

feed = feedparser.parse(python_wiki_rss_url)

for entry in feed['entries']:
    try:
        if entry['content'][0]['value'].find(u'征') > -1:
            print entry['link']
        if entry['title'].find(u'征') > -1:
            print entry['link']
    except:
        continue