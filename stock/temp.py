__author__ = 'yu'

from util import get_all_stock, get_stock_history_by_date, c


def scan(stock):
    pot1 = get_stock_history_by_date(stock, '2015-10-08')
    pot2 = get_stock_history_by_date(stock, '2015-10-09')
    pot3 = get_stock_history_by_date(stock, '2015-10-12')
    pot4 = get_stock_history_by_date(stock, '2015-10-13')
    pot5 = get_stock_history_by_date(stock, '2015-10-14')

    if pot1 and pot2 and pot3 and pot4 and pot5:
        if 'rong_all_balance' in pot1:
            if pot1['rong_all_balance'] < pot2['rong_all_balance'] < pot3['rong_all_balance'] < pot4['rong_all_balance'] < pot5['rong_all_balance']:
                print stock


if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('002'):
            scan(stock)