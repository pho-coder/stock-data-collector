#!/usr/bin/env python3
import sys, os, shutil, time
import utils
import numpy as np
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sdc')
    parser.add_argument('-m', '--manual', help='manual or not', action='store_true')
    parser.add_argument('-dp', '--data_path', help='data path')
    parser.add_argument('-d', '--dt', help='date')
    parser.add_argument('-t', '--tp', help='type: hs300s, one', default='hs300s')
    args = parser.parse_args()
    print(args)

    data_path = args.data_path
    dt = args.dt
    manual = args.manual
    tp = args.tp
    print(data_path, dt, manual, tp)
    if data_path == None or dt == None or manual == None:
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

    if tp == 'hs300s':
        # hs300s daily download
        utils.save_hs300s_ticks_to_csv(today_data_path, dt, data_path + '/hs300s.csv', manual)
