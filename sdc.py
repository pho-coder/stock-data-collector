#!/usr/bin/env python3
import sys
import utils

if __name__ == '__main__':
    print("hi")
    sys.exit(0)
    argv = sys.argv
    data_path = argv[1] if len(argv) >= 2 else './data'
    dt = argv[2] if len(argv) >= 3 else time.strftime('%Y-%m-%d')
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
