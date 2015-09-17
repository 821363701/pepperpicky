__author__ = 'yu'

import Tkinter as tk
import thread
import time
from datetime import datetime
from daily_monitor_simple import Stock


def data_thread(all_stock):
    while True:
        result = []
        for stock in all_stock:
            result.append(stock.get_price())

        global mw
        mw.update(result)
        time.sleep(1)


class MainWindow(tk.Frame):
    def __init__(self, master, title):
        tk.Frame.__init__(self, master)
        self.master.title(title)

        self.grid()
        self.create_widgets()
        self.insert_list()

    def create_widgets(self):
        self.stock_list = tk.Listbox(self, width=40)
        self.stock_list.grid()

        self.var_time = tk.StringVar()
        self.label_time = tk.Label(self, textvariable=self.var_time)
        self.label_time.grid()
        self.var_time.set(str(datetime.now()))

        self.quit_btn = tk.Button(self, text='quit', command=self.quit)
        self.quit_btn.grid()

    def insert_list(self):
        self.stock_list.insert('end', 'hello')

    def update(self, result):
        self.var_time.set(str(datetime.now()))

        self.stock_list.delete(0, self.stock_list.size())
        for i in result:
            self.stock_list.insert('end', i)


if __name__ == "__main__":
    all_stock = []
    with open('buy_rate.dat', 'r') as fp:
        for line in fp.readlines():
            stock, name = line.split('  ')
            all_stock.append(Stock(stock, name.rstrip().decode('utf8')))

    global mw
    main_tk = tk.Tk()
    mw = MainWindow(main_tk, "stock")

    thread.start_new_thread(data_thread, (all_stock,))
    tk.mainloop()