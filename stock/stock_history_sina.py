__author__ = 'yu'

from pymongo import MongoClient
from util import get_all_stock, get_stock_price, boll_daily

c = MongoClient('121.199.5.143').stock

for stock in get_all_stock():
    print stock

    price = get_stock_price(stock)

    # today, yesterday, current, high, low
    today = float(price[1])
    yesterday = float(price[2])
    current = float(price[3])
    high = float(price[4])
    low = float(price[5])
    name = price[0].split('"')[-1]
    date = price[30]
    volume = price[8]

    c.history.update({
        'date': date,
        'stock': stock
    }, {
        '$set': {
            'date': date,
            'open': today,
            'high': high,
            'low': low,
            'close': current,
            'volume': volume,
            'adj': current,
            'stock': stock
        }
    }, upsert=True)

    # calc boll 20
    boll_daily(stock)
