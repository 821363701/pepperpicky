__author__ = 'yu'

import requests
import logging
import time
from datetime import datetime
from utils import send_mail

logging.basicConfig(filename='stock.log', level=logging.INFO)

TEMPLATE_URL = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'
STOCK_SH = 'sh000001'


class Stock(object):
    def __init__(self):
        self.price_count = 10
        self.price_list = []
        self.current_status = ''

    def __get_stock_price(self, stock):
        r = requests.get(TEMPLATE_URL.format(stock))
        # today, yesterday, current, high, low
        price = r.text.split(',')
        return float(price[1]), float(price[2]), float(price[3]), float(price[4]), float(price[5])

    def __judge_stock_price(self):
        diff = self.price_list[0] - self.price_list[-1]

        forward = '+'
        if diff < 0:
            diff = -diff
            forward = '-'

        rate = diff / self.price_list[0]
        if rate > 0.001:
            send_mail('{}{}%'.format(forward, str(rate*100)[:5]))

    def __judge_by_average(self):
        total = 0.0
        for i in self.price_list:
            total += i
        avg = total / len(self.price_list)

        diff = self.price_list[-1] - avg

        forward = '+'
        if diff < 0:
            diff = -diff
            forward = '-'

        rate = diff / avg * 100
        logging.info('{}{}% {}'.format(forward, str(rate)[:5], self.current_status))
        if rate > 0.1:
            send_mail('{}{}% {}'.format(forward, str(rate)[:5], self.current_status))

    def start(self):
        while True:
            try:
                hour = datetime.now().hour
                if 9 < hour < 12 or 13 < hour < 15:
                    (today, yesterday, current, high, low) = self.__get_stock_price(STOCK_SH)

                    if len(self.price_list) == self.price_count:
                        self.price_list.pop(0)

                    self.price_list.append(current)
                    self.current_status = str((current - yesterday)/yesterday * 100)[:6] + '%'
                    self.__judge_by_average()
                else:
                    self.price_list = []
            except Exception, e:
                logging.error(e)
            finally:
                time.sleep(5)

    def test(self):
        self.price_list = [5131.881, 5131.881, 5131.881, 5131.881, 5000.425]
        self.__judge_stock_price()

if __name__ == '__main__':
    p = Stock()
    p.start()
    # p.test()