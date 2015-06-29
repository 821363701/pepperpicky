__author__ = 'yu'

import requests
import logging
import time
import math
from datetime import datetime
from utils import send_mail

logging.basicConfig(filename='stock.log', level=logging.INFO)

TEMPLATE_URL = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'
STOCK_SH = 'sh000001'
STOCK_SZ = 'sz399001'
STOCK_002055 = 'sz002055'
STOCK_002657 = 'sz002657'



class Stock(object):
    METHOD_DIFF = 0
    METHOD_AVG = 1

    def __init__(self, method=METHOD_AVG):
        if method == Stock.METHOD_AVG:
            self.__method_judge = self.__judge_by_average
            self.judge_line = 0.1
        else:
            self.__method_judge = self.__judge_by_diff
            self.judge_line = 0.1

        self.sleep_time = 5
        self.price_count = 5
        self.price_list = []
        self.current_status = ''

    def __get_stock_price(self, stock):
        r = requests.get(TEMPLATE_URL.format(stock))
        # today, yesterday, current, high, low
        price = r.text.split(',')
        return float(price[1]), float(price[2]), float(price[3]), float(price[4]), float(price[5])

    def __judge(self, rate):
        title = '{}% {}'.format(str(rate)[:5], self.current_status)
        logging.info(title)
        if abs(rate) > self.judge_line:
            send_mail(title)

    def __judge_by_diff(self):
        rate = (self.price_list[-1] - self.price_list[0]) / self.price_list[0] * 100
        self.__judge(rate)

    def __judge_by_average(self):
        avg = math.fsum(self.price_list) / len(self.price_list)
        rate = (self.price_list[-1] - avg) / avg * 100
        self.__judge(rate)

    def start(self, stock):
        while True:
            try:
                hour = datetime.now().hour
                if 9 < hour < 12 or 13 < hour < 15:
                    (today, yesterday, current, high, low) = self.__get_stock_price(stock)

                    if len(self.price_list) == self.price_count:
                        self.price_list.pop(0)

                    self.price_list.append(current)
                    self.current_status = str((current - yesterday)/yesterday * 100)[:6] + '%'
                    self.__method_judge()
                else:
                    self.price_list = []
            except Exception, e:
                logging.error(e)
            finally:
                time.sleep(self.sleep_time)

    def test(self):
        self.price_list = [5131.881, 5131.881, 5131.881, 5131.881, 5000.425]
        print math.fsum(self.price_list)

if __name__ == '__main__':
    p = Stock()
    p.start(STOCK_SH)
    # p.test()