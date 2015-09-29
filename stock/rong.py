__author__ = 'yu'

import requests
import pygal
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
from util import get_stock_history_by_date, rate
from stock_history import get_history

url_rong = 'http://www.szse.cn/szseWeb/FrontController.szse'


def data_standard(l):
    avg = float(sum(l)/len(l))

    new_l = []
    for i in l:
        new_l.append(i/avg)

    return new_l


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


# print get_rong_sz('002230', '2015-09-14')


def calc_rong_svg(stock_code):
    x = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []

    for i in range(30):
        day = datetime.now()+timedelta(days=-i)
        date = day.strftime('%Y-%m-%d')

        result = get_rong_sz(stock_code, date)
        if result:
            price = get_stock_history_by_date(stock_code+'.SZ', date)
            if not price:
                price = {
                    'volume': 0,
                    'close': 0
                }

            print '{}\t{}\t{}\t{}\t{}'.format(date, result[2], result[3], price['volume'], price['close'])

            x.append(date[6:])
            y1.append(int(result[2].replace(',', '')))
            y2.append(int(result[3].replace(',', '')))
            y3.append(float(price['volume']))
            y4.append(float(price['close']))

    x.reverse()
    y1.reverse()
    y2.reverse()
    y3.reverse()
    y4.reverse()

    line_chart = pygal.Line(width=1600, height=800)
    line_chart.title = 'rongzi'
    line_chart.x_labels = x
    line_chart.add('rongzi', data_standard(y1))
    line_chart.add('rongzi_balance', data_standard(y2))
    line_chart.add('volume', data_standard(y3))
    line_chart.add('close', data_standard(y4), secondary=True)
    line_chart.render_to_file(stock_code+'.svg')


if __name__ == '__main__':
    get_history('002', 'SZ', '024', '2015-09-01', '2015-09-28')
    calc_rong_svg('002024')