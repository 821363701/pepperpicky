# coding=utf-8
__author__ = 'yuxizhou'

from pymongo import MongoClient

c = MongoClient('121.199.5.143').pick

for i in c.all_topic.find({}):
    if i['keyword'] != u'上海':
        print i['keyword']

        c.target_info.insert({
            'topic_id': i['topic_id'],
            'topic_title': i['topic_title'],
            'keyword': i['keyword'],
            'founder_id': i['founder_id'],
            'timestamp': i['timestamp'],
            'source': i['source'],
        })