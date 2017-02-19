#!/usr/bin/env python3
import sys, os, shutil
import utils

if __name__ == '__main__':
    argv = sys.argv
    data_path = argv[1] if len(argv) >= 2 else './data'
    dt = argv[2] if len(argv) >= 3 else time.strftime('%Y-%m-%d')
    manual = True if len(argv) >= 4 else False
    print(data_path, dt, manual)
    if not os.path.exists(data_path):
        print(data_path + ' NOT exists!')
        sys.exit(1)
    today_data_path = data_path + '/' + dt
    today_data_hs300 = today_data_path + '/hs300.csv'
    if os.path.exists(today_data_path):
        print('rm ' + today_data_path)
        shutil.rmtree(today_data_path)
        os.mkdir(today_data_path)
    else:
        os.mkdir(today_data_path)
    while True:
        if not manual:
            if int(time.strftime('%H', time.localtime())) > 20:
                break
        if not os.path.exists(today_data_hs300):
            print('download hs300')
            utils.save_hs300s_to_csv(today_data_hs300, dt)
        break
        # save_hs300s_tick_to_csv(today_path, dt)
        # if os.path.isfile(today_path + '/finish'):
        #     break
        # else:
        #     print('NO finish')
        #     time.sleep(60)
