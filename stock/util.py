__author__ = 'yuxizhou'

import requests
from pymongo import MongoClient

sina_api = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'
c = MongoClient('121.199.5.143').stock

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


def get_stock_name_from_mongo(stock):
    return c.info.find_one({
        'stock': stock
    })['name']


def get_all_stock():
    return c.history.distinct('stock')

def get_stock_history_by_date(stock, date):
    return c.history.find_one({
        'stock': stock,
        'date': date
    })

def rate(a, b):
    return (a - b) / b * 100

# get_stock_name('600000.SS')