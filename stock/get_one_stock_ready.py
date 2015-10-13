__author__ = 'yu'

from stock_history import get_many_day
from stock_rong_history_to_db import save_rong_for_days_before


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'need stock code'
    else:
        stock_code = sys.argv[1]+'.SZ'

        get_many_day(stock_code, '2015-09-01', '2015-09-30')
        save_rong_for_days_before(stock_code, 100)
