__author__ = 'yu'

import pygal


def data_standard(l):
    avg = float(sum(l)/len(l))

    new_l = []
    for i in l:
        new_l.append(i/avg)

    return new_l


x = []
y1 = []
y2 = []
y3 = []
y4 = []
with open('sz_rong_all_60days.dat', 'r') as fp:
    for line in fp:
        parts = eval(line.strip())

        try:
            x.append('1')
            y1.append(int(parts[0].replace(',', '')))
            y2.append(int(parts[1].replace(',', '')))
            # y3.append(float(parts[4]))
            # y4.append(float(parts[5]))
        except:
            print parts

x.reverse()
y1.reverse()
y2.reverse()
y3.reverse()
y4.reverse()

line_chart = pygal.Line(width=1600, height=800)
line_chart.title = 'rongzi'
line_chart.x_labels = x
line_chart.add('rongzi', data_standard(y1))
line_chart.add('rongzi_balance', data_standard(y2))
# line_chart.add('open', y3, secondary=True)
# line_chart.add('close', y4, secondary=True)
line_chart.render_to_file('test.svg')

