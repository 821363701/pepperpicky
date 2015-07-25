__author__ = 'yu'

'''
{
    "_id" : ObjectId("55b0d687e694aa0dbaa6779d"),
    "stock" : "600000.SS",
    "date" : "2015-07-22",
    "open" : 16.33,
    "close" : 16.16,
    "high" : 16.38,
    "low" : 16.15,
    "volume" : 120352700,
    "adj" : 16.16
}

'''

from pymongo import MongoClient
from util import get_stock_name_from_mongo, get_all_stock, get_stock_history_by_date, rate

c = MongoClient('121.199.5.143').stock
stocks = get_all_stock()


def test():
    for stock in stocks:
        day = c.history.find_one({
            'stock': stock,
            'date': '2015-07-24'
        })

        rate = (day['close'] - day['open']) / day['open'] * 100
        if abs(rate) > 9:
            name = get_stock_name_from_mongo(stock)
            print u'{} {} {}'.format(name, stock, rate)


def find_sline():
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

            if day['date'] == "2015-07-24":
                now = day

        if high and low and now:
            high_rate = (high['high'] - now['close']) / now['close'] * 100
            low_rate = (now['close'] - low['low']) / low['low'] * 100

            sline = low['low'] + (high['high'] - low['low']) / 8

            if now['close'] < sline:
                name = c.info.find_one({
                    'stock': stock
                })['name']

                print u"{} {} -- {}({})[{}] {}[{}] {}({})[{}]".format(stock, name, high['high'], high_rate, high['date'],
                                                    now['close'], now['date'], low['low'], low_rate, low['date'])
        else:
            print "error {}".format(stock)


def find_rate():
    for stock in stocks:
        try:
            print stock
            first_open = get_stock_history_by_date(stock, '2015-07-09')['low']
            last_close = get_stock_history_by_date(stock, '2015-07-24')['close']

            r = rate(last_close, first_open)
            print '{}  {}'.format(stock, r)
        except:
            continue


if __name__ == '__main__':
    # find_sline()
    # test()
    find_rate()