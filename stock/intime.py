# coding=utf-8
__author__ = 'yu'

from util import get_all_stock, get_stock_price, rate, get_stock_history_by_date, calc_s_line

# tmp = ['000911.SZ', '000560.SZ', '000662.SZ', '000718.SZ', '000686.SZ']
#
# rank = []
# for stock in get_all_stock():
#     start = get_stock_history_by_date(stock, '2015-07-29')
#     if start:
#         start_open = start['close']
#     else:
#         continue
#
#     price = get_stock_price(stock)
#
#     # today, yesterday, current, high, low
#     today = float(price[1])
#     yesterday = float(price[2])
#     current = float(price[3])
#     high = float(price[4])
#     low = float(price[5])
#     name = price[0].split('"')[-1]
#
#     if today == '0.00':
#         continue
#
#     r = rate(current, start_open)
#
#     if r > 15:
#         print u'{}  {}  {}'.format(name, stock, r)
#         continue
#     else:
#         continue
#
#     if 35 > r > 10:
#         print stock
#         rank.append((stock, r, name))
#
# ranked = sorted(rank, key=lambda r: r[1])
# for stock, total_rate, name in ranked:
#     s = calc_s_line(stock)
#
#     price = get_stock_price(stock)
#     yesterday = float(price[2])
#     current = float(price[3])
#
#     today_rate = rate(current, yesterday)
#
#     print u'{}\t{}\t{}\t{}\t{}'.format(str(total_rate)[:4], str(today_rate)[:4], s, name, stock)
#

a = '''西藏天路  600326.SS  16.7215815486
西藏旅游  600749.SS  19.7235513025
西藏城投  600773.SS  16.7121418827
连云港  601008.SS  15.2112676056
深物业A  000011.SZ  20.9616829452
特力Ａ  000025.SZ  18.6666666667
荣安地产  000517.SZ  16.3719711853
三湘股份  000863.SZ  20.9809264305
银亿股份  000981.SZ  151.655629139
长白山  603099.SS  20.1385452746
云南旅游  002059.SZ  15.4963680387
北斗星通  002151.SZ  20.9949184274
奥普光电  002338.SZ  17.3222912353
齐星铁塔  002359.SZ  148.464163823
青龙管业  002457.SZ  16.5186500888
金利科技  002464.SZ  20.993343574
恒基达鑫  002492.SZ  52.5357607282
山东矿机  002526.SZ  21.0526315789
蒙发利  002614.SZ  21.0380622837
长青集团  002616.SZ  20.9964412811
亿利达  002686.SZ  21.0420841683
索菱股份  002766.SZ  21.010719755
国恩股份  002768.SZ  15.6093307172
文科园林  002775.SZ  15.4260528893
理工监测  002322.SZ  19.590268886
科迪乳业  002770.SZ  17.7500973141
众兴菌业  002772.SZ  18.6009955462'''

for line in a.split('\n'):
    stock = line.split('  ')[1]

    price = get_stock_price(stock)
    yesterday = float(price[2])
    current = float(price[3])
    name = price[0].split('"')[-1]

    r = rate(current, yesterday)

    if r < 9:
        print u'{} {} {}'.format(stock, r, name)