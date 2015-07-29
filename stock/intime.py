__author__ = 'yu'

from util import get_all_stock, get_stock_price, rate


# rank = []
for stock in get_all_stock():
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

    r = rate(current, yesterday)
    if r > 5.0:
        print u'{}\t{}\t{}'.format(r, stock, name)

    # rank.append((stock, r, name))

# ranked = sorted(rank, key=lambda r: r[1])
# for rn, rr, name in ranked:
#     print u'{}\t{}\t{}'.format(rn, rr, name)