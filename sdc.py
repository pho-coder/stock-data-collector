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
        print(data_path + 'hs300s.csv NOT exists!')
        sys.exit(1)
    today_data_path = data_path + '/' + dt
    today_data_hs300 = today_data_path + '/hs300.csv'
    hs300_list = list(pd.read_csv(data_path + '/hs300s.csv', dtype={'code': np.str}).code)
    if os.path.exists(today_data_path):
        print('rm ' + today_data_path)
        shutil.rmtree(today_data_path)
        os.mkdir(today_data_path)
    else:
        os.mkdir(today_data_path)
    hs300_count = len(hs300_list)
    while True:
        if not manual:
            if int(time.strftime('%H', time.localtime())) > 20:
                break
        if not os.path.exists(today_data_hs300):
            print('download hs300')
            utils.save_hs300s_to_csv(today_data_hs300, dt)
        for one in hs300_list:
            if utils.save_one_tick_to_csv(one, today_data_path, dt):
                hs300_list.remove(one)
        if len(hs300_list) == hs300_count:
            print('NO download one more, left ' + str(hs300_count))
            left_list = open(today_data_path +'/left', 'w')
            for one in hs300_list:
                left_list.write(one + '\n')
            left_list.close()
            finish = open(today_data_path + '/finish', 'w')
            finish.close()
            break
        else:
            hs300_count = len(hs300_list)
        time.sleep(10)
        # save_hs300s_tick_to_csv(today_path, dt)
        # if os.path.isfile(today_path + '/finish'):
        #     break
        # else:
        #     print('NO finish')
        #     time.sleep(60)
