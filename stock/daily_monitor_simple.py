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
        self.last_price = None

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

        r = str(rate(current, yesterday))[:4]

        forward = '--'
        if not self.last_price:
            forward = '--'
        elif current > self.last_price:
            forward = '/\\'
        elif current < self.last_price:
            forward = '\/'
        else:
            forward = '--'

        self.last_price = current
        return u'{} {} ({}% {}){}'.format(self.name, self.stock, r, current, forward)


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

        clear()

        for l in result:
            if not l:
                continue

            print(l, end='\n')

        print('')
        print(datetime.now())

        time.sleep(1)
