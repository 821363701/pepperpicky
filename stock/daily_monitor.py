from __future__ import print_function
__author__ = 'yu'

import os
import time
clear = lambda: os.system('clear')
from util import get_stock_price, rate
from datetime import datetime


class Stock:
    def __init__(self, stock, name):
        self.stock = stock
        self.name = name
        self.five_price = []
        self.available = True
        self.reopen = False

    def get_price(self):
        price = get_stock_price(self.stock)

        # today, yesterday, current, high, low
        today = float(price[1])
        yesterday = float(price[2])
        current = float(price[3])
        high = float(price[4])
        low = float(price[5])
        volume = float(price[8])
        name = price[0].split('"')[-1]

        if today == '0.00':
            return u'{}(0.00)'.format(self.stock)

        r = rate(current, yesterday)

        if not self.available and r < 9.9:
            self.reopen = True

        if r > 9.9:
            self.available = False
        else:
            self.available = True

        if len(self.five_price) == 5:
            self.five_price.pop(0)
        self.five_price.append(r)

        if len(self.five_price) > 1:
            forward = self.five_price[-1] - self.five_price[-2]
        else:
            forward = '0.00'

        r = str(r)[:4]
        forward = str(forward)[:4]

        buy = int(price[10]) + int(price[12]) + int(price[14]) + int(price[16]) + int(price[18])
        sell = int(price[20]) + int(price[22]) + int(price[24]) + int(price[26]) + int(price[28])

        if sell == 0:
            bs = float(buy) / float(1)
            if volume > 0:
                buy_rate = buy /volume
        else:
            bs = float(buy) / float(sell)

        if bs > 1:
            bs = str(bs)[:4]
            return u'{}({} {})({})'.format(self.stock, r, forward, bs)
        else:
            return u''


if __name__ == '__main__':
    all_stock = []
    with open('buy_rate.dat', 'r') as fp:
        for line in fp.readlines():
            stock, name = line.split('  ')
            all_stock.append(Stock(stock, name))

    while True:
        result = []
        for stock in all_stock:
            result.append(stock.get_price())
            # if stock.reopen:
            #     result.append(stock.get_price()+'**')
            # else:
            #     if stock.available:
            #         result.append(stock.get_price())
            #     else:
            #         result.append(stock.get_price()+'#')

        clear()

        index = 0
        for l in result:
            if not l:
                continue

            if (index+1) % 3 == 0:
                print(l, end='\n')
            else:
                print(l, end='\t')

            index += 1

        print('')
        print(datetime.now())

        time.sleep(10)