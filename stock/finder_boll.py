__author__ = 'yuxizhou'

from util import get_all_stock, get_stock_history_by_date


if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('000') or stock.startswith('002'):
            r = get_stock_history_by_date(stock, '2015-10-16')

            if not r:
                continue

            if r['close'] == 0.0 or r['volume'] == 0:
                continue

            if 'dn' not in r:
                continue

            print stock

            bar_up = r['mb']
            bar_down = r['dn'] + (r['mb'] - r['dn'])/2

            if bar_down < r['close'] < bar_up:
                print stock