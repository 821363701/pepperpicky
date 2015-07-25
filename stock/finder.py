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

from util import get_stock_name_from_mongo, get_all_stock, get_stock_history_by_date, rate, get_stock_days, is_stop_now

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
        days = get_stock_days(stock)

        if days.count() < 10:
            continue

        if is_stop_now(stock):
            continue

        high = None
        low = None
        now = None

        for day in days:
            if (not high) or (high['high'] < day['high']):
                high = day

            if (not low) or (low['low'] > day['low']):
                low = day

            if day['date'] == "2015-07-24":
                now = day

        if high and low and now:
            x = high['high'] - low['low']
            y = now['close'] - low['low']
            if y == 0.0 or x == 0.0:
                continue

            s = x / y

            if s > 10.0:
                continue

            all.append((stock, s))
        else:
            print "error {}".format(stock)

    ranked = sorted(all, key=lambda r: r[1])
    count = 0.0
    for stock, s in ranked:
        print '{} {}'.format(s, stock)
        count += s
    print count/len(all)


def find_sline():
    for stock in stocks:
        days = get_stock_days(stock)

        if days.count() < 10:
            continue

        high = None
        low = None
        now = None

        for day in days:
            if (not high) or (high['high'] < day['high']):
                high = day

            if (not low) or (low['low'] > day['low']):
                low = day

            if day['date'] == "2015-07-24":
                now = day

        if high and low and now:
            high_rate = (high['high'] - now['close']) / now['close'] * 100
            low_rate = (now['close'] - low['low']) / low['low'] * 100

            s_line = low['low'] + (high['high'] - low['low']) / 8

            if now['close'] < s_line:
                if is_stop_now(stock):
                    continue

                name = get_stock_name_from_mongo(stock)
                print u"{} {} {}".format(s_line, stock, name)
        else:
            print "error {}".format(stock)


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


if __name__ == '__main__':
    count_avg_s_line()
    # find_sline()
    # test()
    # find_rate()