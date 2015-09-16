__author__ = 'yu'

import requests
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
from util import get_stock_history_by_date, rate

url_rong = 'http://www.szse.cn/szseWeb/FrontController.szse'


def get_rong_sz(stock_code, stock_date):
    r = requests.post(url_rong, {
        'ACTIONID': 7,
        'AJAX': 'AJAX-TRUE',
        'CATALOGID': '1837_xxpl',
        'TABKEY': 'tab1',
        'txtDate': stock_date,
        'txtZqdm': stock_code,
        'REPORT_ACTION': 'search'
    })

    try:
        soup = BeautifulSoup(r.text)
        rong_stock = soup.findAll('tr', {'class': 'cls-data-tr'})[1]
        code, name, rongzi_buy, rongzi_balance, rongquan_sell_liang, rongquan_balance_liang, rongquan_balance, rong_all_balance = [i.text for i in rong_stock]
        return code, name, rongzi_buy, rongzi_balance, rongquan_sell_liang, rongquan_balance_liang, rongquan_balance, rong_all_balance
    except:
        return None
    finally:
        r.close()


# print get_rong_sz('002476', '2015-09-14')

for i in range(60):
    day = datetime.now()+timedelta(days=-i)
    date = day.strftime('%Y-%m-%d')

    result = get_rong_sz('002476', date)
    if result:
        price = get_stock_history_by_date('002476.SZ', date)
        r = rate(price['close'], price['open'])
        r = str(r)[:4]
        print '{}\t{}\t{}\t{}\t{}\t{}'.format(date, result[2], result[3], r, price['open'], price['close'])