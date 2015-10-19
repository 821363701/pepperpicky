__author__ = 'yuxizhou'

import requests
import math
from pymongo import MongoClient, DESCENDING
from datetime import datetime

sina_api = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'
c = MongoClient('121.199.5.143').stock


def get_stock_price(stock):
    '''
    get stock price

    :param stock:
    :return:
    0: name
    1: today
    2: yesterday
    3: current
    4: high
    5: low
    6: buy 1
    7: sell 1
    8: volume
    9: turnover

    '''
    parts = stock.split('.')
    if parts[1] == 'SS':
        r = requests.get(sina_api.format('sh'+parts[0]))
    else:
        r = requests.get(sina_api.format('sz'+parts[0]))

    result = r.text.split(',')

    r.close()

    return result


def get_stock_name(stock):
    parts = stock.split('.')
    if parts[1] == 'SS':
        r = requests.get(sina_api.format('sh'+parts[0]))
    else:
        r = requests.get(sina_api.format('sz'+parts[0]))

    result = r.text.split(',')

    name = result[0].split('"')[-1]

    r.close()

    return name


def is_stop_now(stock):
    parts = stock.split('.')
    if parts[1] == 'SS':
        r = requests.get(sina_api.format('sh'+parts[0]))
    else:
        r = requests.get(sina_api.format('sz'+parts[0]))

    result = r.text.split(',')

    name = result[1] == '0.00'

    r.close()

    return name


def get_stock_name_from_mongo(stock):
    return c.info.find_one({
        'stock': stock
    })['name']


def get_all_stock():
    return c.history.distinct('stock')


def get_stock_days(stock):
    return c.history.find({
        'stock': stock
    })


def get_stock_history_by_date(stock, date):
    result = c.history.find_one({
        'stock': stock,
        'date': date
    })

    return result


def rate(a, b):
    return (a - b) / b * 100


def calc_s_line(stock):
    days = get_stock_days(stock)

    if days.count() < 10:
        return None

    if is_stop_now(stock):
        return None

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
        x = high['high'] - low['low']
        y = now['close'] - low['low']
        if y == 0.0 or x == 0.0:
            return None

        return x / y
    else:
        return None


def boll(stock, days=20):
    curser = c.history.find({
        'stock': stock,
        'date': {
            '$gt': '2015-08-01'
        }
    }).sort('date')

    result = []
    for day in curser:
        if day['close'] != 0.0:
            result.append(day)

    aviable = len(result) - days + 1
    for i in range(aviable):
        ma = 0.0
        for d in result[i:i+days]:
            ma += d['close']
        ma /= days

        md = 0.0
        for d in result[i:i+days]:
            md += pow(d['close'] - ma, 2)
        md = math.sqrt(md/days)

        mb = ma
        up = mb + 2 * md
        dn = mb - 2 * md

        c.history.update({
            'stock': stock,
            'date': result[i+days-1]['date']
        }, {
            '$set': {
                'ma': ma,
                'mb': mb,
                'up': up,
                'dn': dn
            }
        })


def boll_daily(stock, days=20):
    curser = c.history.find({
        'stock': stock,
        'close': {
            '$ne': 0.0
        }
    }).sort('date', DESCENDING)

    result = []
    for day in curser.limit(20):
        if day['close'] != 0.0:
            result.append(day)

    aviable = len(result) - days + 1
    for i in range(aviable):
        ma = 0.0
        for d in result[i:i+days]:
            ma += d['close']
        ma /= days

        md = 0.0
        for d in result[i:i+days]:
            md += pow(d['close'] - ma, 2)
        md = math.sqrt(md/days)

        mb = ma
        up = mb + 2 * md
        dn = mb - 2 * md

        c.history.update({
            'stock': stock,
            'date': result[0]['date']
        }, {
            '$set': {
                'ma': ma,
                'mb': mb,
                'up': up,
                'dn': dn
            }
        })


def kdj(stock):
    curser = c.history.find({
        'stock': stock,
        'date': {
            '$gt': '2015-08-01'
        }
    }).sort('date')

    result = []
    for day in curser:
        if day['close'] != 0.0:
            result.append(day)

    last_k = 50.0
    last_d = 50.0
    for r in result:
        if r['high'] == r['low']:
            continue

        rsv = (r['close'] - r['low']) / (r['high'] - r['low']) * 100

        k = 2/3*last_k + 1/3*rsv
        d = 2/3*last_d + 1/3*k
        j = 3*k - 2*d

        c.history.update({
            'stock': stock,
            'date': r['date']
        }, {
            '$set': {
                'rsv': rsv,
                'k': k,
                'd': d,
                'j': j
            }
        })

        last_k = k
        last_d = d


if __name__ == "__main__":
    kdj('000777.SZ')

    # boll('000777.SZ')

    # for stock in get_all_stock():
    #     if stock.startswith('000') or stock.startswith('002'):
    #         print stock
    #         boll(stock)