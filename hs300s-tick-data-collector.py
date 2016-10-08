#!/usr/bin/env python3
import sys
import time
import tushare as ts


def get_hs300s_code():
    return ts.get_hs300s().code


def get_one_stock_tick(cd, dt):
    return ts.get_tick_data(cd, date=dt).assign(code=cd).assign(date=dt)


def save_hs300s_tick_to_csv(path, dt):
    for one_code in get_hs300s_code():
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        print(one_code)
        get_one_stock_tick(one_code, dt).to_csv(path)

if __name__ == '__main__':
    # argv = sys.argv
    # if len(argv) < 6:
    #     print("argv error!")
    #     sys.exit(1)
    # user = argv[1]
    # password = argv[2]
    # ip = argv[3]
    # db = argv[4]
    # date = argv[5]
    save_hs300s_tick_to_csv("./a.csv", "2016-09-30")
