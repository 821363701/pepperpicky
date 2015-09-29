__author__ = 'yu'

from pymongo import MongoClient
from rong import get_rong_sz

c = MongoClient('121.199.5.143').stock

stocks = c.history.distinct('stock')
for stock in stocks:
    if stock.find('002') == 0:
        result = get_rong_sz(stock[:6], '2015-09-28')
        if result:
            rongzi1 = int(result[2].replace(',', ''))
            rongzi2 = 0

            r0914 = get_rong_sz(stock[:6], '2015-09-25')
            if r0914:
                rongzi2 = int(r0914[2].replace(',', ''))

            if rongzi1 > 2*rongzi2:
                print '{} {} {}'.format(stock, rongzi2, rongzi1)
        else:
            continue