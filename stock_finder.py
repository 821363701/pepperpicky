__author__ = 'yu'

'''
{
    "_id" : ObjectId("55b0d687e694aa0dbaa6779d"),
    "high" : 16.38,
    "volume" : 120352700,
    "low" : 16.15,
    "date" : "2015-07-22",
    "close" : 16.16,
    "stock" : "600000.SS",
    "open" : 16.33,
    "adj" : 16.16
}

'''

from pymongo import MongoClient

c = MongoClient('121.199.5.143').stock

stocks = c.history.distinct('stock')

for stock in stocks:
    first_open = c.history.find_one({
        'stock': stock,
        'date': '2015-07-09'
    })['open']

    last_close = c.history.find_one({
        'stock': stock,
        'date': '2015-07-22'
    })['close']

    rate = (last_close - first_open) / first_open * 100

    if rate < 10 and rate != 0.0:
        print '{}  {}'.format(stock, rate)