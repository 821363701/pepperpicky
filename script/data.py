__author__ = 'yuxizhou'

from pymongo import MongoClient

c = MongoClient('121.199.5.143').pick

func = '''
function( curr, result ) {
     result.total += 1;
 }
'''


for i in c.all_topic.group(['keyword'], None, {'total': 0}, reduce=func):
    print u'{}\t{}'.format(i['total'], i['keyword'])