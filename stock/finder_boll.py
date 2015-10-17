__author__ = 'yuxizhou'

from util import get_all_stock, get_stock_history_by_date

'''
000016.SZ
000425.SZ
002424.SZ
002465.SZ
002471.SZ
002489.SZ
002512.SZ
002547.SZ
002563.SZ
002568.SZ
002617.SZ
002640.SZ
002650.SZ
002651.SZ
002697.SZ
002707.SZ
002329.SZ
'''

if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('000') or stock.startswith('002'):
            r1 = get_stock_history_by_date(stock, '2015-10-08')
            r2 = get_stock_history_by_date(stock, '2015-10-09')
            r3 = get_stock_history_by_date(stock, '2015-10-12')
            r4 = get_stock_history_by_date(stock, '2015-10-13')
            r5 = get_stock_history_by_date(stock, '2015-10-14')
            r6 = get_stock_history_by_date(stock, '2015-10-15')
            r7 = get_stock_history_by_date(stock, '2015-10-16')

            if not r7:
                continue

            if r7['close'] == 0.0 or r7['volume'] == 0:
                continue

            if 'dn' not in r7:
                continue

            if r7['up'] > r6['up'] > r5['up'] > r4['up'] > r3['up'] > r2['up'] > r1['up']:
                if r7['mb'] > r6['mb'] > r5['mb'] > r4['mb'] > r3['mb'] > r2['mb'] > r1['mb']:
                    if r7['dn'] > r6['dn'] > r5['dn'] > r4['dn'] > r3['dn'] > r2['dn'] > r1['dn']:
                        print stock