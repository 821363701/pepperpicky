__author__ = 'yuxizhou'

from pymongo import MongoClient
from util import get_stock_name

c = MongoClient('121.199.5.143').stock

stocks = c.history.distinct('stock')
for stock in stocks:
    name = get_stock_name(stock)
    c.info.insert({
        'name': name,
        'stock': stock
    })

    print u'{} {}'.format(stock, name)