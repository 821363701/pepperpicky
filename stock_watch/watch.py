__author__ = 'yu'

import time
import requests

TEMPLATE_URL = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'


def __get_stock_price(stock):
    r = requests.get(TEMPLATE_URL.format(stock))
    # today, yesterday, current, high, low
    price = r.text.split(',')
    buy = int(price[10]) + int(price[12]) + int(price[14]) + int(price[16]) + int(price[18])
    sell = int(price[20]) + int(price[22]) + int(price[24]) + int(price[26]) + int(price[28])
    return float(price[1]), float(price[2]), float(price[3]), float(price[4]), float(price[5]), buy, sell


def watch(stock, sleep_time=5):
    while True:
        (today, yesterday, current, high, low, buy, sell) = __get_stock_price(stock)
        current_percent = str((current - yesterday)/yesterday * 100)[:6] + '%'
        if buy > sell:
            print '{}: {} [{}>>{}] {}'.format(stock, current, buy, sell, current_percent)
        else:
            print '{}: {} [{}<<{}] {}'.format(stock, current, buy, sell, current_percent)
        time.sleep(sleep_time)


