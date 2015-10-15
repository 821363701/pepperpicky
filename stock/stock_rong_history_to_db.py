__author__ = 'yu'

from datetime import datetime, timedelta
from rong import get_rong_sz
from util import get_all_stock, c

'''
002024.SZ
002028.SZ
002050.SZ
002108.SZ
002223.SZ
002237.SZ
002242.SZ
002261.SZ
002262.SZ
002266.SZ
002269.SZ
002375.SZ
002393.SZ
002414.SZ
002416.SZ
002475.SZ
002476.SZ
002594.SZ
'''


def to_db(stock, date, result):
    code, name, rongzi_buy, rongzi_balance, rongquan_sell_liang, rongquan_balance_liang, rongquan_balance, rong_all_balance = result
    print code

    c.history.update({
        'date': date,
        'stock': stock
    }, {
        '$set': {
            'rongzi_buy': rongzi_buy,
            'rongzi_balance': rongzi_balance,
            'rongquan_sell_liang': rongquan_sell_liang,
            'rongquan_balance_liang': rongquan_balance_liang,
            'rongquan_balance': rongquan_balance,
            'rong_all_balance': rong_all_balance
        }
    })


def save_rong_for_days_before(stock, day_before):
    for i in range(1, day_before):
        day = datetime.now()+timedelta(days=-i)
        date = day.strftime('%Y-%m-%d')
        result = get_rong_sz(stock[:6], date)
        if result:
            to_db(stock, date, result)

if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('000') or stock.startswith('002'):
            save_rong_for_days_before(stock, 6)

    # save_rong_for_days_before('002476.SZ', 100)