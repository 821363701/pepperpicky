__author__ = 'yu'

import requests
import logging
import time
from datetime import datetime
from utils import send_mail

# logging.basicConfig(filename='stock.log', level=logging.INFO)

TEMPLATE_URL = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'
STOCK_SH = 'sh000001'
STOCK_ZCJK = 'sz002657'


class Stock(object):
    def __init__(self):
        self.five_price = []

    def __get_stock_price(self, stock):
        r = requests.get(TEMPLATE_URL.format(stock))

        return float(r.text.split(',')[3])

    def __judge_stock_price(self):
        diff = self.five_price[0] - self.five_price[4]
        if diff > 0:
            rate = diff / self.five_price[0]
            if rate > 0.005:
                send_mail('-' + str(rate*100)[:5] + '%')

    def start(self):
        while True:
            try:
                hour = datetime.now().hour
                if 9 < hour < 12 or 13 < hour < 15:
                    price = self.__get_stock_price(STOCK_SH)

                    print price

                    if len(self.five_price) < 5:
                        self.five_price.append(price)
                    else:
                        self.five_price.pop(0)
                        self.five_price.append(price)

                        self.__judge_stock_price()
                else:
                    self.five_price = []
            except Exception, e:
                logging.error(e)
            finally:
                time.sleep(10)

    def test(self):
        self.five_price = [5131.881, 5131.881, 5131.881, 5131.881, 5000.425]
        self.__judge_stock_price()

if __name__ == '__main__':
    p = Stock()
    p.start()
    # p.test()