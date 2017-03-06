#!/usr/bin/env python3
import sys, os, shutil, time
import utils
import numpy as np
import pandas as pd
import cli.app

@CommandLineApp(argv=["-v"])
def sdc():
    pass


if __name__ == '__main__':
    # argv = sys.argv
    # data_path = argv[1] if len(argv) >= 2 else './data'
    # dt = argv[2] if len(argv) >= 3 else time.strftime('%Y-%m-%d')
    # manual = True if len(argv) >= 4 else False
    # print(data_path, dt, manual)
    # if not os.path.exists(data_path + '/hs300s.csv'):
    #     print(data_path + '/hs300s.csv NOT exists!')
    #     sys.exit(1)
    # today_data_path = data_path + '/' + dt
    # today_data_hs300 = today_data_path + '/hs300.csv'
    # hs300s = utils.read_hs300s(data_path + '/hs300s.csv')
    # hs300s_codes = list(hs300s.code)
    # if os.path.exists(today_data_path):
    #     print('rm ' + today_data_path)
    #     shutil.rmtree(today_data_path)
    #     os.mkdir(today_data_path)
    # else:
    #     os.mkdir(today_data_path)

    # hs300s daily download
   # utils.save_hs300s_ticks_to_csv(today_data_path, dt, data_path + '/hs300s.csv', manual)
    sdc.run()
