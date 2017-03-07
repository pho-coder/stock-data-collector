#!/usr/bin/env python3
import sys
import os
import time
from datetime import datetime, timedelta
import shutil
import tushare as ts
import pandas as pd
import numpy as np
# from sqlalchemy import create_engine


def get_hs300s_code():
    return ts.get_hs300s().code


def read_hs300s(file):
    return pd.read_csv(file, dtype={'code': np.str,
                                    'name': np.str,
                                    'date': np.str,
                                    'weight': np.str})


def get_one_stock_tick(cd, dt):
    return ts.get_tick_data(cd,
                            date=dt,
                            retry_count=600,
                            pause=0.1).assign(code=cd).assign(date=dt)


def get_hs300_history_data(start_dt, end_dt):
    ts.get_hist_data('hs300', start=start_dt, end=end_dt)


def save_hs300s_to_csv(path, dt):
    df = ts.get_hist_data('hs300', start=dt, end=dt)
    if not df.empty:
        df.to_csv(path)


def save_one_tick_to_csv(code, f, dt):
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print(code, dt)
    data = get_one_stock_tick(code, dt)
    if not data.empty and not data.iloc[0][0] == 'alert("当天没有数据");':
        data.to_csv(f, index=False)
        return True
    else:
        print('NO DATA')
        print(data)
        return False


def save_one_tick_some_days_to_csv(code, code_data_path, start_dt, end_dt):
    one_day = timedelta(days=1)
    one_date = datetime.strptime(start_dt, '%Y-%m-%d')
    end_date = datetime.strptime(end_dt, '%Y-%m-%d')
    while True:
        if one_date > end_date:
            break
        one_dt = one_date.strftime('%Y-%m-%d')
        save_one_tick_to_csv(code, code_data_path + '/' + one_dt + '.csv', one_dt)
        one_date = one_date + one_day


def save_hs300s_ticks_to_csv(today_data_path, dt, hs300s_file, manual):
    today_data_hs300 = today_data_path + '/hs300.csv'
    hs300s = read_hs300s(hs300s_file)
    hs300s_codes = list(hs300s.code)
    hs300_count = len(hs300s_codes)
    finish_list = open(today_data_path + '/list', 'w')
    while True:
        if not manual:
            if int(time.strftime('%H', time.localtime())) > 21:
                break
        if not os.path.exists(today_data_hs300):
            print('download hs300')
            save_hs300s_to_csv(today_data_hs300, dt)
        for one_code in hs300s_codes:
            if save_one_tick_to_csv(one_code, today_data_path + '/' + code + '.csv', dt):
                one_info = hs300s[hs300s.code == one_code]
                finish_list.write(one_code + ',' +
                                  str(one_info.iloc[0]['weight']) + ',' +
                                  str(one_info.iloc[0]['name']) + '\n')
                finish_list.flush()
                hs300s_codes.remove(one_code)
        if len(hs300s_codes) <= 20 and len(hs300s_codes) == hs300_count:
            print('NO download one more, left ' + str(hs300_count))
            left_list = open(today_data_path + '/left', 'w')
            for one_code in hs300s_codes:
                left_list.write(one_code + '\n')
            left_list.close()
            finish = open(today_data_path + '/finish', 'w')
            finish.close()
            break
        else:
            hs300_count = len(hs300s_codes)
        time.sleep(60)
    finish_list.close()


def save_hs300s_tick_to_mysql(tb, eg, dt):
    for one_code in get_hs300s_code():
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        print(one_code)
        get_one_stock_tick(one_code, dt).to_sql(tb, eg, if_exists='append')


if __name__ == '__main__':
    argv = sys.argv
    path = argv[1] if len(argv) >= 2 else './data'
    dt = argv[2] if len(argv) >= 3 else time.strftime('%Y-%m-%d')
    manual = True if len(argv) >= 4 else False
    download_hs300_only = True if len(argv) >= 5 else False
    if not os.path.exists(path):
        print(path + ' NOT exists!')
        sys.exit(1)
    today_path = path + '/' + dt
    today_hs300 = path + '/SH000300.' + dt
    while True:
        if not manual:
            if int(time.strftime('%H', time.localtime())) > 20:
                break
        if not os.path.exists(today_hs300):
            print('download hs300')
            save_hs300s_to_csv(today_hs300, dt)
            if download_hs300_only:
                break
        if os.path.exists(today_hs300) and download_hs300_only:
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
