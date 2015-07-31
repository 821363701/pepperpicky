__author__ = 'yu'

from pymongo import MongoClient
from bson.code import Code
from stock_history import get_many_day

reducer = Code("""
                function(obj, prev){
                  prev.count++;
                }
                """)

c = MongoClient('121.199.5.143').stock

result = c.history.group(key={"stock": 1}, condition={}, initial={"count": 0}, reduce=reducer)
for doc in result:
    # print doc['count']
    if doc['count'] != 43:
        print '{}  {}'.format(doc['stock'], doc['count'])
        get_many_day(doc['stock'], '2015-06-01', '2015-07-29')