__author__ = 'yu'

from pymongo import MongoClient
from rong import get_rong_sz

c = MongoClient('121.199.5.143').stock

stocks = c.history.distinct('stock')
for stock in stocks:
    if stock.find('002') == 0 or stock.find('000') == 0:
        result = get_rong_sz(stock[:6], '2015-09-16')
        if result:
            rongzi1 = int(result[2].replace(',', ''))
            rongzi2 = 0
            rongzi3 = 0

            r0914 = get_rong_sz(stock[:6], '2015-09-15')
            if r0914:
                rongzi2 = int(r0914[2].replace(',', ''))

            r0911 = get_rong_sz(stock[:6], '2015-09-14')
            if r0911:
                rongzi3 = int(r0911[2].replace(',', ''))

            avg = (rongzi2 + rongzi3 + rongzi1)/3
            if rongzi1 > avg:
                print '{} {} {} {}'.format(stock, rongzi3, rongzi2, rongzi1)
        else:
            continue