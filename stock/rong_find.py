__author__ = 'yu'

from pymongo import MongoClient
from rong import get_rong_sz

c = MongoClient('121.199.5.143').stock

stocks = c.history.distinct('stock')
for stock in stocks:
    if stock.find('002') == 0 or stock.find('000') == 0:
        result = get_rong_sz(stock[:6], '2015-09-15')
        if result:
            rongzi0915 = int(result[2].replace(',', ''))
            rongzi0914 = 0
            rongzi0911 = 0

            r0914 = get_rong_sz(stock[:6], '2015-09-14')
            if r0914:
                rongzi0914 = int(r0914[2].replace(',', ''))

            r0911 = get_rong_sz(stock[:6], '2015-09-11')
            if r0911:
                rongzi0911 = int(r0914[2].replace(',', ''))

            avg = (rongzi0914 + rongzi0911 + rongzi0915)/3
            if rongzi0915 > avg:
                print '{} {} {} {}'.format(stock, rongzi0911, rongzi0914, rongzi0915)
        else:
            continue