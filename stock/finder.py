__author__ = 'yu'

'''
{
    "_id" : ObjectId("55b0d687e694aa0dbaa6779d"),
    "stock" : "600000.SS",
    "date" : "2015-07-22",
    "open" : 16.33,
    "close" : 16.16,
    "high" : 16.38,
    "low" : 16.15,
    "volume" : 120352700,
    "adj" : 16.16
}

'''

from util import get_stock_name_from_mongo, get_all_stock, get_stock_history_by_date, rate, get_stock_days, is_stop_now, calc_s_line

stocks = get_all_stock()


def test():
    for stock in stocks:
        day = get_stock_history_by_date(stock, '2015-07-24')

        rate = (day['close'] - day['open']) / day['open'] * 100
        if abs(rate) > 9:
            name = get_stock_name_from_mongo(stock)
            print u'{} {} {}'.format(name, stock, rate)


def count_avg_s_line():
    all = []
    for stock in stocks:
        s = calc_s_line(stock)

        if not s:
            continue

        if s > 10.0:
            continue

        all.append((stock, s))

    ranked = sorted(all, key=lambda r: r[1])
    count = 0.0
    for stock, s in ranked:
        print '{} {}'.format(s, stock)
        count += s
    print count/len(all)


def find_sline():
    for stock in stocks:
        if not stock.startswith('002'):
            continue

        days = get_stock_days(stock)

        if days.count() < 10:
            continue

        high = None
        low = None
        now = None

        for day in days:
            if day['close'] == 0.0:
                continue

            if (not high) or (high['close'] < day['close']):
                high = day

            if (not low) or (low['close'] > day['close']):
                low = day

            if day['date'] == "2015-11-06":
                now = day

        if high and low and now:
            name = get_stock_name_from_mongo(stock)
            print u'{}\t{}\t{}\t{}\t{}'.format(high['close'], low['close'], now['close'], stock, name)

            # high_rate = (high['close'] - now['close']) / now['close'] * 100
            # low_rate = (now['close'] - low['close']) / low['close'] * 100
            #
            # s_line = low['close'] + (high['close'] - low['close']) / 8
            #
            # if now['close'] < s_line:
            #     name = get_stock_name_from_mongo(stock)
            #     print u"{} {} {}".format(s_line, stock, name)
        else:
            pass


def find_rate():
    rank = []

    for stock in stocks:
        try:
            first_open = get_stock_history_by_date(stock, '2015-07-09')['low']
            last_close = get_stock_history_by_date(stock, '2015-07-24')['close']

            r = rate(last_close, first_open)
            rank.append((stock, r))
        except:
            continue

    ranked = sorted(rank, key=lambda r: r[1])
    for rn, rr in ranked:
        name = get_stock_name_from_mongo(rn)
        print u'{} {} {}'.format(name, rn, rr)


def find_last_week_up_most():
    rank = []
    for stock in stocks:
        if not stock.startswith('002'):
            continue

        try:
            first_open = get_stock_history_by_date(stock, '2015-09-30')['close']
            last_close = get_stock_history_by_date(stock, '2015-11-06')['close']

            r = rate(last_close, first_open)
            rank.append((stock, r))
        except:
            continue

    ranked = sorted(rank, key=lambda r: r[1])
    for rn, rr in ranked:
        print u'{} {}'.format(rn, rr)


if __name__ == '__main__':
    # count_avg_s_line()
    # find_sline()
    # test()
    # find_rate()
    find_last_week_up_most()

