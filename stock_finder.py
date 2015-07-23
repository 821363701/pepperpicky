__author__ = 'yu'

# stock_code, first_day, first_open, first_close, last_day, last_open, last_close

with open('a', 'r') as fp:
    lines = fp.readlines()

for line in lines:
    parts = line.split('\t')
    code = parts[0]
    first_open = float(parts[2])
    last_close = float(parts[6])

    rate = (last_close - first_open) / first_open * 100

    if rate < 10:
        print '{} {}%'.format(code, rate)