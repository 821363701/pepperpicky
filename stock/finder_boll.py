__author__ = 'yuxizhou'

from util import get_all_stock, boll


if __name__ == '__main__':
    for stock in get_all_stock():
        if stock.startswith('002'):
            mb, up, dn, now = boll(stock, 10)
            if now != 0.0:
                line1 = dn + (mb-dn)/2
                line2 = dn + (mb-dn)/3
                if line2 < now < line1:
                    print '{} {} {} {} {}'.format(stock, mb, up, dn, now)