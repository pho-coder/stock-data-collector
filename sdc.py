#!/usr/bin/env python3
import sys, os, shutil, time
import utils
import numpy as np
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sdc')
    parser.add_argument('-m', '--manual', help='manual or not; default False', action='store_true')
    parser.add_argument('-dp', '--data_path', help='data path')
    parser.add_argument('-d', '--dt', help='date, default today', default=time.strftime('%Y-%m-%d'))
    parser.add_argument('-t', '--tp', help='type: hs300s, one, today; default hs300s\n' +
                        'sdc -t today -dp $STOCK_DATA_PATH -c 000002', default='hs300s')
    parser.add_argument('-sd', '--start_dt', help='one stock start date, default two weeks before', default=time.strftime('%Y-%m-%d', time.localtime(time.time() - 24*60*60*14)))
    parser.add_argument('-ed', '--end_dt', help='one stock end date, default one day before', default=time.strftime('%Y-%m-%d', time.localtime(time.time() - 24*60*60*1)))
    parser.add_argument('-c', '--code', help='one stock code')
    args = parser.parse_args()
    print(args)

    data_path = args.data_path
    tp = args.tp

    if tp == 'hs300s':
        dt = args.dt
        manual = args.manual
        print(data_path, dt, manual)
        if data_path is None or dt is None or manual is None:
            print("data_path, dt or manual is None")
            sys.exit(1)
        if not os.path.exists(data_path + '/hs300s.csv'):
            print(data_path + '/hs300s.csv NOT exists!')
            sys.exit(1)
        today_data_path = data_path + '/' + dt
        if os.path.exists(today_data_path):
            print('rm ' + today_data_path)
            shutil.rmtree(today_data_path)
            os.mkdir(today_data_path)
        else:
            os.mkdir(today_data_path)
        # hs300s daily download
        utils.save_hs300s_ticks_to_csv(today_data_path, dt, data_path + '/hs300s.csv', manual)
    elif tp == 'one':
        start_dt = args.start_dt
        end_dt = args.end_dt
        code = args.code
        print(data_path, start_dt, end_dt)
        if data_path is None or start_dt is None or end_dt is None or code is None:
            print("data_path, start_dt, end_dt or code is None")
            sys.exit(1)
        if not os.path.exists(data_path):
            print(data_path + ' NOT EXISTS!')
            sys.exit(1)
        code_data_path = data_path + '/' + code
        if os.path.exists(code_data_path):
            print('rm ' + code_data_path)
            shutil.rmtree(code_data_path)
            os.mkdir(code_data_path)
        else:
            os.mkdir(code_data_path)
        utils.save_one_tick_some_days_to_csv(code, code_data_path, start_dt, end_dt)
    elif tp == 'today':
        code = args.code
        print(data_path, code)
        if data_path is None or code is None:
            print('data path or code is None')
            sys.exit(1)
        if not os.path.exists(data_path):
            print(data_path + ' NOT EXISTS!')
            sys.exit(1)
        code_data_today = data_path + '/' + code + '.' + time.strftime('%Y-%m-%d')
        utils.save_one_tick_today(code, code_data_today)
