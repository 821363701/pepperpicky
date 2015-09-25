__author__ = 'yu'

import Tkinter as tk
import thread
import time
from Queue import Queue, Empty
from datetime import datetime
from daily_monitor_simple import Stock

result_queue = Queue()


def data_thread(all_stock):
    while True:
        result = []
        for stock in all_stock:
            result.append(stock.get_price())

        global mw
        mw.update(result)
        time.sleep(1)


def stock_thread(s, i):
    while True:
        global result_queue
        result_queue.put((i, s.get_price()))

        time.sleep(1)


def update_thread():
    global result_queue
    global mw
    while True:
        i, r = result_queue.get()
        mw.update_one(i, r)


def update_callback():
    global result_queue
    global mw
    while True:
        try:
            item = result_queue.get(False)
            i, r = item
            mw.update_one(i, r)
        except Empty:
            break
    mw.after(100, update_callback)


class MainWindow(tk.Frame):
    def __init__(self, master, title):
        tk.Frame.__init__(self, master)
        self.master.title(title)

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.stock_list = tk.Listbox(self, width=40)
        self.stock_list.grid()

        self.var_time = tk.StringVar()
        self.label_time = tk.Label(self, textvariable=self.var_time)
        self.label_time.grid()
        self.var_time.set(str(datetime.now()))

        self.quit_btn = tk.Button(self, text='quit', command=self.quit)
        self.quit_btn.grid()

    def update(self, result):
        self.var_time.set(str(datetime.now()))

        self.stock_list.delete(0, self.stock_list.size())
        for i in result:
            self.stock_list.insert('end', i)

    def update_one(self, i, r):
        self.var_time.set(datetime.now().strftime('%H:%M:%S'))

        self.stock_list.delete(i, i)
        self.stock_list.insert(i, r)


if __name__ == "__main__":
    all_stock = []
    with open('main_index.config', 'r') as fp:
        for line in fp.readlines():
            stock, name = line.split('  ')
            all_stock.append(Stock(stock, name.rstrip().decode('utf8')))

    global mw
    main_tk = tk.Tk()
    mw = MainWindow(main_tk, "stock")


    # thread.start_new_thread(data_thread, (all_stock,))
    for index, stock in enumerate(all_stock):
        thread.start_new_thread(stock_thread, (stock, index))
    # thread.start_new_thread(update_thread, ())
    mw.after(100, update_callback)

    tk.mainloop()