#!/usr/bin/env python3
import sys
import time
import tushare as ts
from sqlalchemy import create_engine

def get_hs300s_code():
    return ts.get_hs300s().code

def get_one_stock_tick(cd, dt):
    return ts.get_tick_data(cd, date=dt).assign(code=cd).assign(date=dt)

def save_hs300s_tick_to_mysql(tb, eg, dt):
    for one_code in get_hs300s_code():
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        print(one_code)
        get_one_stock_tick(one_code, dt).to_sql(tb, eg, if_exists='append')

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 6:
        print("argv error!")
        sys.exit(1)
    user = argv[1]
    password = argv[2]
    ip = argv[3]
    db = argv[4]
    date = argv[5]
    table = 'tick_data'
    engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + ip + '/' + db + '?charset=utf8')
    save_hs300s_tick_to_mysql(table, engine, date)
