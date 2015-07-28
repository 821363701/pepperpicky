# coding=utf-8
__author__ = 'yu'

import requests
from pymongo import MongoClient
from datetime import datetime
from util import get_stock_history_by_date

'''
请求地址
http://ichart.yahoo.com/table.csv?s=&a=&b=&c=&d=&e=&f=&g=d&ignore=.csv
参数
s — 股票名称
a — 起始时间，月
b — 起始时间，日
c — 起始时间，年
d — 结束时间，月
e — 结束时间，日
f — 结束时间，年
g — 时间周期。Example: g=w, 表示周期是‘周’。d->‘日’(day), w->‘周’(week)，m->‘月’(mouth)，v->‘dividends only’
一定注意月份参数，其值比真实数据-1。如需要9月数据，则写为08。
示例
查询浦发银行2010.09.25 – 2010.10.8之间日线数据
http://ichart.yahoo.com/table.csv?s=600000.SS&a=08&b=25&c=201000&d=09&e=8&f=2010&g=d

yahoo的api是国际性的，是支持国内沪深股市的，但代码稍微变动一下，如浦发银行的代号是：600000.SS。规则是：上海市场末尾加.ss，深圳市场末尾加.sz。

沪市A股票买卖的代码是以600、601或603打头
深市A股票买卖的代码是以000打头

curl 'http://ichart.yahoo.com/table.csv?s=601211.SS&a=05&b=01&c=2015&d=06&e=24&f=2015&g=d'
curl 'http://ichart.yahoo.com/table.csv?s=601211.SS&a=06&b=28&c=2015&d=06&e=28&f=2015&g=d'

'''

c = MongoClient('121.199.5.143').stock

sina_api = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'
base_api = 'http://ichart.yahoo.com/table.csv?s={}&a={}&b={}&c={}&d={}&e={}&f={}&g=d'
stock_all = [('600', 'SS'), ('601', 'SS'), ('603', 'SS'), ('000', 'SZ'), ('002', 'SZ')]
base_stock = '{}{}'


def is_exist(where, code):
    if where == 'SS':
        r = requests.get(sina_api.format('sh'+code))
    else:
        r = requests.get(sina_api.format('sz'+code))

    if len(r.text.split(',')) > 2:
        print '{} is exists'.format(code)
        r.close()
        return True
    else:
        print '{} is NOT exists'.format(code)
        r.close()
        return False


def tran_date_month(month):
    m = str(int(month) - 1)
    if len(m) == 1:
        return '0'+m
    else:
        return m


def get_history(pre, where, a, date_from, date_to, con=False):
    if not is_exist(where, base_stock.format(pre, a)):
        return

    stock_code = base_stock.format(pre, a) + '.' + where

    if con:
        is_saved = get_stock_history_by_date(stock_code, date_to)
        if is_saved:
            return

    date_from_parts = date_from.split('-')
    date_to_parts = date_to.split('-')
    stock_api = base_api.format(stock_code,
                                tran_date_month(date_from_parts[1]), date_from_parts[2], date_from_parts[0],
                                tran_date_month(date_to_parts[1]), date_to_parts[2], date_to_parts[0])

    try:
        print 'start load {} {}'.format(stock_code, str(datetime.now()))
        r = requests.get(stock_api)
        result = r.text

        lines = result.split('\n')
        for line in lines[1:]:
            if line:
                parts = line.split(',')
                if len(parts) >= 7:
                    c.history.update({
                        'date': parts[0],
                        'stock': stock_code
                    }, {
                        'date': parts[0],
                        'open': float(parts[1]),
                        'high': float(parts[2]),
                        'low': float(parts[3]),
                        'close': float(parts[4]),
                        'volume': float(parts[5]),
                        'adj': float(parts[6]),
                        'stock': stock_code
                    }, upsert=True)
        r.close()
    except:
        print 'except when {}'.format(stock_code)


def get_all():
    for prefix in stock_all:
        for i in range(0, 1000):
            a = str(i)
            if len(a) == 1:
                a = '00'+a
            elif len(a) == 2:
                a = '0'+a
            elif len(a) == 3:
                pass
            else:
                continue

            pre, where = prefix
            date = '2015-07-28'

            get_history(pre, where, a, date, date, True)


def get_one(stock, date):
    get_history(stock[:3], stock[-2:], stock[3:6], date, date)


def get_many_day(stock, date_from, date_to):
    get_history(stock[:3], stock[-2:], stock[3:6], date_from, date_to)


def get_002():
    for i in range(0, 1000):
        a = str(i)
        if len(a) == 1:
            a = '00'+a
        elif len(a) == 2:
            a = '0'+a
        elif len(a) == 3:
            pass
        else:
            continue

        pre = '002'
        where = 'SZ'

        get_history(pre, where, a, '2015-06-01', '2015-07-24')


if __name__ == '__main__':
    get_all()


