# coding=utf-8
__author__ = 'yu'

from util import get_all_stock, get_stock_price, rate, get_stock_history_by_date, calc_s_line


def find():
    count = 0
    rank = []
    for stock in get_all_stock():
        price = get_stock_price(stock)

        # today, yesterday, current, high, low
        today = float(price[1])
        yesterday = float(price[2])
        current = float(price[3])
        high = float(price[4])
        low = float(price[5])
        volume = float(price[8])
        name = price[0].split('"')[-1]

        if today == '0.00':
            continue

        r = rate(current, yesterday)

        buy = int(price[10]) + int(price[12]) + int(price[14]) + int(price[16]) + int(price[18])
        sell = int(price[20]) + int(price[22]) + int(price[24]) + int(price[26]) + int(price[28])

        if sell == 0:
            bs = float(buy) / float(1)
        else:
            bs = float(buy) / float(sell)

        if volume > 0:
            buy_rate = buy / volume

        ###############

        if r > 9.9:
            count += 1
        else:
            if name.find(u'中') == 0:
                print u'{} {} {}'.format(stock, name, r)

    print count

        # if buy_rate > 0.1:
        #         print u'{}  {}  {}  {}'.format(stock, name, r, buy_rate)

        # if bs > 10 and r < 9.9:
        #     print u'{}  {}  {}  {}'.format(stock, name, r, bs)


find()