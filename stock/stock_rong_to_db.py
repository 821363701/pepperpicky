__author__ = 'yu'

from datetime import datetime, timedelta
from rong import get_rong_sz
from util import get_all_stock, c


if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('000') or stock.startswith('002'):
            day = datetime.now()+timedelta(days=-1)
            date = day.strftime('%Y-%m-%d')
            code, name, rongzi_buy, rongzi_balance, rongquan_sell_liang, rongquan_balance_liang, rongquan_balance, rong_all_balance = get_rong_sz(stock[:6], date)

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