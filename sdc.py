#!/usr/bin/env python3
import sys, os, shutil, time
import utils
import numpy as np
import pandas as pd

if __name__ == '__main__':
    argv = sys.argv
    data_path = argv[1] if len(argv) >= 2 else './data'
    dt = argv[2] if len(argv) >= 3 else time.strftime('%Y-%m-%d')
    manual = True if len(argv) >= 4 else False
    print(data_path, dt, manual)
    if not os.path.exists(data_path + '/hs300s.csv'):
        print(data_path + '/hs300s.csv NOT exists!')
        sys.exit(1)
    today_data_path = data_path + '/' + dt
    today_data_hs300 = today_data_path + '/hs300.csv'
    hs300s = utils.read_hs300s(data_path + '/hs300s.csv')
    hs300s_codes = list(hs300s.code)
    if os.path.exists(today_data_path):
        print('rm ' + today_data_path)
        shutil.rmtree(today_data_path)
        os.mkdir(today_data_path)
    else:
        os.mkdir(today_data_path)
    hs300_count = len(hs300s_codes)
    finish_list = open(today_data_path + '/list', 'w')
    while True:
        if not manual:
            if int(time.strftime('%H', time.localtime())) > 20:
                break
        if not os.path.exists(today_data_hs300):
            print('download hs300')
            utils.save_hs300s_to_csv(today_data_hs300, dt)
        for one in hs300s_codes:
            if utils.save_one_tick_to_csv(one, today_data_path, dt):
                one_info = hs300s[hs300s.code == one]
                finish_list.write(one + ',' +
                                  one_info.iloc[0]['weight'] + ',' +
                                  one_info.iloc[0]['name'] + '\n')
                finish_list.flush()
                hs300s_codes.remove(one)
        if len(hs300s_codes) == hs300_count and len(hs300s_codes) <= 20:
            print('NO download one more, left ' + str(hs300_count))
            left_list = open(today_data_path +'/left', 'w')
            for one in hs300s_codes:
                left_list.write(one + '\n')
            left_list.close()
            finish = open(today_data_path + '/finish', 'w')
            finish.close()
            break
        else:
            hs300_count = len(hs300s_codes)
        time.sleep(60)
    finish_list.close()
