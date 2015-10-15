__author__ = 'yu'

from util import get_all_stock, get_stock_history_by_date


if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('002'):
            price1 = get_stock_history_by_date(stock, '2015-09-30')['open']
            price2 = get_stock_history_by_date(stock, '2015-10-14')['close']

            if price1 == 0:
                continue

            bar = float(price2) / price1

            print '{}\t{}'.format(stock, bar)