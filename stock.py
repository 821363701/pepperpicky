# coding=utf-8
__author__ = 'yu'

import requests
import logging
import time
import math
import traceback
from datetime import datetime
from utils import send_mail

logging.basicConfig(filename='stock.log', level=logging.INFO)

TEMPLATE_URL = 'http://hq.sinajs.cn/etag.php?_=0.9219840362202376&list={}'
STOCK_SH = 'sh000001'
STOCK_SZ = 'sz399001'
STOCK_002055 = 'sz002055'
STOCK_002657 = 'sz002657'

STOCK = {
    'sh000001': u'上证',
    'sz002476': u'宝莫',
    'sz000926': u'福星'
}


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
        self.price_count = 10
        self.current_status = ''
        self.current_stock = ''

        self.price_single_list = {}
        for single in STOCK:
            self.price_single_list[single] = []

    def __get_stock_price(self, stock):
        r = requests.get(TEMPLATE_URL.format(stock))
        # today, yesterday, current, high, low
        price = r.text.split(',')
        return float(price[1]), float(price[2]), float(price[3]), float(price[4]), float(price[5])

    def __judge(self, rate):
        title = u'{}% {} {}'.format(str(rate)[:5], self.current_status, STOCK[self.current_stock])
        logging.info(title)
        if abs(rate) > self.judge_line:
            send_mail(title.encode('utf-8'))

    def __judge_by_diff(self):
        rate = (self.price_single_list[self.current_stock][-1] - self.price_single_list[self.current_stock][0]) / self.price_single_list[self.current_stock][0] * 100
        self.__judge(rate)

    def __judge_by_average(self):
        avg = math.fsum(self.price_single_list[self.current_stock]) / len(self.price_single_list[self.current_stock])
        rate = (self.price_single_list[self.current_stock][-1] - avg) / avg * 100
        self.__judge(rate)

    def start(self):
        while True:
            try:
                hour = datetime.now().hour
                if 9 < hour < 15:
                    for single in STOCK:
                        self.current_stock = single
                        (today, yesterday, current, high, low) = self.__get_stock_price(single)

                        if len(self.price_single_list[single]) == self.price_count:
                            self.price_single_list[single].pop(0)
                            
                        self.price_single_list[single].append(current)
                        self.current_status = str((current - yesterday)/yesterday * 100)[:6] + '%'

                        self.__method_judge()
                else:
                    self.price_single_list = {}
                    for single in STOCK:
                        self.price_single_list[single] = []
            except Exception, e:
                traceback.print_exc()
                logging.error(e)
            finally:
                time.sleep(self.sleep_time)


if __name__ == '__main__':
    p = Stock()
    p.start()
    # p.test()