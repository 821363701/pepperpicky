__author__ = 'yu'

from util import get_all_stock, get_stock_history_by_date, c, rate

'''
002016.SZ
002065.SZ
002078.SZ
002095.SZ
002142.SZ
002151.SZ
002154.SZ
002311.SZ
002378.SZ
002385.SZ
002407.SZ
002410.SZ
002429.SZ
002482.SZ
'''


def i(s):
    return float(s.replace(',', ''))


def scan(stock):
    # pot1 = get_stock_history_by_date(stock, '2015-10-08')
    # pot2 = get_stock_history_by_date(stock, '2015-10-09')
    # pot3 = get_stock_history_by_date(stock, '2015-10-12')
    pot4 = get_stock_history_by_date(stock, '2015-10-13')
    pot5 = get_stock_history_by_date(stock, '2015-10-14')
    pot6 = get_stock_history_by_date(stock, '2015-10-15')

    if pot4 and pot5 and pot6:
        if 'rong_all_balance' in pot6 and pot6['close'] != 0.0:
            if i(pot4['rong_all_balance']) > i(pot5['rong_all_balance']) > i(pot6['rong_all_balance']):
                r = str(rate(i(pot4['rong_all_balance']), i(pot6['rong_all_balance'])))[:5]
                print '{} {}'.format(stock, r)


if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('002'):
            scan(stock)