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
import requests

sina_api = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'

c = MongoClient('121.199.5.143').stock

stocks = c.history.distinct('stock')

for stock in stocks:
    days = c.history.find({
        'stock': stock
    })

    high = None
    low = None
    now = None

    for day in days:
        if (not high) or (high['high'] < day['high']):
            high = day

        if (not low) or (low['low'] > day['low']):
            low = day

        if day['date'] == "2015-07-22":
            now = day

    if high and low and now:
        high_rate = (high['high'] - now['close']) / now['close'] * 100
        low_rate = (now['close'] - low['low']) / low['low'] * 100

        sline = low['low'] + (high['high'] - low['low']) / 8

        if now['close'] < sline:
            parts = stock.split('.')
            if parts[1] == 'SS':
                r = requests.get(sina_api.format('sh'+parts[0]))
            else:
                r = requests.get(sina_api.format('sz'+parts[0]))
            name = r.text.split(',')[0].split('"')[1]
            if r.text.split(',')[1] != '0.00':
                print u"{} {} -- {}({})[{}] {}[{}] {}({})[{}]".format(stock, name, high['high'], high_rate, high['date'],
                                                    now['close'], now['date'], low['low'], low_rate, low['date'])
            r.close()
    else:
        print "error {}".format(stock)



# for stock in stocks:
#     first_open = c.history.find_one({
#         'stock': stock,
#         'date': '2015-07-09'
#     })['open']
#
#     last_close = c.history.find_one({
#         'stock': stock,
#         'date': '2015-07-22'
#     })['close']
#
#     rate = (last_close - first_open) / first_open * 100
#
#     if rate < 10 and rate != 0.0:
#         print '{}  {}'.format(stock, rate)