__author__ = 'yuxizhou'

from pymongo import MongoClient
from const import *
import time

mongo_client = MongoClient('mongodb://pepper:821363701@ds029950.mongolab.com:29950/pepper').pepper

with open('target_info', 'r') as fp:
    for line in fp:
        split_line = line.split('\t')

        if len(split_line) == 5:
            ts = split_line[4]
        else:
            ts = ''

        topic_id = split_line[0].split('topic')[1][1:-1]
        founder_id = split_line[2][8:-6]

        a = time.time()
        mongo_client.test_target_info.insert({
            'topic_id': topic_id,
            'topic_title': split_line[3],
            'keyword': split_line[1],
            'founder_id': founder_id,
            'timestamp': ts,
            'source': SOURCE_DOUBAN,
        })
        b = time.time()
        print (b-a)