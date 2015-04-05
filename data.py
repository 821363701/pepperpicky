__author__ = 'yuxizhou'

from pymongo import MongoClient

c = MongoClient('121.199.5.143').pick

func = '''
function( curr, result ) {
     result.total += 1;
 }
'''


for i in c.user_area.group(['people_area'], None, {'total': 0}, reduce=func):
    if i['total'] > 1000:
        print u'{}\t{}'.format(i['total'], i['people_area'])