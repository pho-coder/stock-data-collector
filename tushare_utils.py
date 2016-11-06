#!/usr/bin/env python3
import sys
import os
import time
import shutil
import tushare as ts
# from sqlalchemy import create_engine


def get_hs300s_code():
    return ts.get_hs300s().code


def get_one_stock_tick(cd, dt):
    return ts.get_tick_data(cd,
                            date=dt,
                            retry_count=600,
                            pause=0.1).assign(code=cd).assign(date=dt)


def get_hs300_history_data(start_dt, end_dt):
    ts.get_hist_data('hs300', start=start_dt, end=end_dt)


def save_hs300s_tick_to_csv(path, dt):
    list = open(path + '/list', 'w')
    for one_code in get_hs300s_code():
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        print(one_code)
        data = get_one_stock_tick(one_code, dt)
        if not data.iloc[0][0] == 'alert("当天没有数据");':
            list.write(one_code + '\n')
            list.flush()
            data.to_csv(path + '/' +
                        one_code + '.csv',
                        index=False)
    list.close()
    with open(path + '/list', 'r') as f:
        if f.readline() != '':
            finish = open(path + '/finish', 'w')
            finish.close()


def save_hs300s_tick_to_mysql(tb, eg, dt):
    for one_code in get_hs300s_code():
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        print(one_code)
        get_one_stock_tick(one_code, dt).to_sql(tb, eg, if_exists='append')


if __name__ == '__main__':
    argv = sys.argv
    # if len(argv) < 6:
    #     print("argv error!")
    #     sys.exit(1)
    # user = argv[1]
    # password = argv[2]
    # ip = argv[3]
    # db = argv[4]
    # date = argv[5]
    # table = 'tick_data'
    # engine = create_engine('mysql+pymysql://' + user + ':' +
    #                        password + '@' + ip + '/' + db + '?charset=utf8')
    # save_hs300s_tick_to_mysql(table, engine, date)
    path = argv[1] if len(argv) >= 2 else './data'
    dt = argv[2] if len(argv) >= 3 else time.strftime('%Y-%m-%d')
    if not os.path.exists(path):
        print(path + ' NOT exists!')
        sys.exit(1)
    today_path = path + '/' + dt
    while True:
        if int(time.strftime('%H', time.localtime())) > 20:
            break
        if os.path.exists(today_path):
            print('rm ' + today_path)
            shutil.rmtree(today_path)
            os.mkdir(today_path)
        else:
            os.mkdir(today_path)
        save_hs300s_tick_to_csv(today_path, dt)
        if os.path.isfile(today_path + '/finish'):
            break
        else:
            print('NO finish')
            time.sleep(60)
