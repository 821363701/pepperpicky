__author__ = 'yu'

import time
import requests

TEMPLATE_URL = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'


def __get_stock_price(stock):
    r = requests.get(TEMPLATE_URL.format(stock))
    # today, yesterday, current, high, low
    price = r.text.split(',')
    return float(price[1]), float(price[2]), float(price[3]), float(price[4]), float(price[5])


def watch(stock, sleep_time=5):
    while True:
        try:
            (today, yesterday, current, high, low) = __get_stock_price(stock)
            current_percent = str((current - yesterday)/yesterday * 100)[:6] + '%'
            print '{}: {} {}'.format(stock, current, current_percent)
        except:
            pass
        finally:
            time.sleep(sleep_time)


