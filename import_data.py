__author__ = 'yuxizhou'

from const import *
from pymongo import MongoClient

c = MongoClient('127.0.0.1').pick
# c = MongoClient('192.168.125.150').pick

with open('target_info', 'r') as fp:
    for line in fp:
        split_line = line[:-1].split('\t')

        if len(split_line) == 5:
            ts = split_line[4]
        else:
            ts = ''

        topic_id = split_line[0].split('topic')[1][1:-1]
        founder_id = split_line[2][8:-6]

        c.target_info.insert({
            'topic_id': topic_id,
            'topic_title': split_line[3],
            'keyword': split_line[1],
            'founder_id': founder_id,
            'timestamp': ts,
            'source': SOURCE_DOUBAN,
        })

with open('user_area', 'r') as fp:
    for line in fp:
        split_line = line[:-1].split('\t')

        if len(split_line) != 2:
            continue

        people_id = split_line[0][8:-6]
        people_area = split_line[1]

        c.user_area.insert({
            'people_id': people_id,
            'people_area': people_area
        })

with open('visited_topic', 'r') as fp:
    for line in fp:
        split_line = line[:-1].split('\t')

        if len(split_line) != 2:
            continue

        topic_id = split_line[0].split('/')[-2]
        topic_title = split_line[1]

        c.visited_topic.insert({
            'topic_id': topic_id,
            'topic_title': topic_title
        })

with open('deny_id', 'r') as fp:
    for line in fp:
        deny_id = line[:-1]

        c.deny_id.insert({
            'deny_id': deny_id
        })
