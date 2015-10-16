__author__ = 'yu'

from util import get_all_stock, get_stock_history_by_date, c, rate

'''

10.13 - 10.15 rong_all_balance reduce
002016.SZ 11.29
002065.SZ 3.434
002078.SZ 2.163
002095.SZ 23.97
002142.SZ 1.387
002151.SZ 14.27
002154.SZ 2.417
002241.SZ 5.837
002311.SZ 8.197
002378.SZ 1.164
002385.SZ 1.917
002429.SZ 4.366
002482.SZ 0.359

10.12 - 10.15 rong_all_balance reduce
002241.SZ 7.244
002311.SZ 11.97

'''


def i(s):
    return float(s.replace(',', ''))


def scan(stock):
    # pot1 = get_stock_history_by_date(stock, '2015-10-08')
    # pot2 = get_stock_history_by_date(stock, '2015-10-09')
    pot3 = get_stock_history_by_date(stock, '2015-10-12')
    pot4 = get_stock_history_by_date(stock, '2015-10-13')
    pot5 = get_stock_history_by_date(stock, '2015-10-14')
    pot6 = get_stock_history_by_date(stock, '2015-10-15')

    if pot3 and pot4 and pot5 and pot6:
        if 'rong_all_balance' in pot6 and pot6['close'] != 0.0:
            if i(pot3['rong_all_balance']) > i(pot4['rong_all_balance']) > i(pot5['rong_all_balance']) > i(pot6['rong_all_balance']):
                r = str(rate(i(pot3['rong_all_balance']), i(pot6['rong_all_balance'])))[:5]
                print '{} {}'.format(stock, r)


if __name__ == '__main__':
    # for stock in get_all_stock():
    #     if stock.startswith('002'):
    #         scan(stock)

    for stock in ['002016.SZ', '002065.SZ', '002078.SZ', '002095.SZ', '002142.SZ', '002151.SZ', '002154.SZ', '002241.SZ', '002311.SZ', '002378.SZ', '002385.SZ', '002429.SZ', '002482.SZ']:
        scan(stock)