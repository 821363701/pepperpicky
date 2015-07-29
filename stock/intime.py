# coding=utf-8
__author__ = 'yu'

from util import get_all_stock, get_stock_price, rate, get_stock_history_by_date, calc_s_line

tmp = ['000911.SZ', '000560.SZ', '000662.SZ', '000718.SZ', '000686.SZ']

rank = []
for stock in get_all_stock():
    start = get_stock_history_by_date(stock, '2015-07-27')
    if start:
        start_open = start['open']
    else:
        continue

    price = get_stock_price(stock)

    # today, yesterday, current, high, low
    today = float(price[1])
    yesterday = float(price[2])
    current = float(price[3])
    high = float(price[4])
    low = float(price[5])
    name = price[0].split('"')[-1]

    if today == '0.00':
        continue

    r = rate(current, start_open)
    if 35 > r > 10:
        rank.append((stock, r, name))

ranked = sorted(rank, key=lambda r: r[1])
for stock, total_rate, name in ranked:
    s = calc_s_line(stock)

    price = get_stock_price(stock)
    yesterday = float(price[2])
    current = float(price[3])

    today_rate = rate(current, yesterday)

    print u'{}\t{}\t{}\t{}\t{}'.format(str(total_rate)[:4], str(today_rate)[:4], s, name, stock)