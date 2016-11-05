#!/usr/bin/env python3
import utils
import time
import os
import sys

print(os.getenv('DATA_PATH'))


def deal_data(today_data):
    data = today_data.iloc[0]
    tag = data[0]
    date = data['date'].strftime('%Y-%m-%d')
    open_price = data['open']
    high = data['high']
    low = data['low']
    close = data['close']
    volume = data['volume']
    title_str = 'tag,date,open,high,low,close,volume'
    with open(os.getenv('DATA_PATH') + '/' + tag + '.' + date, 'w') as f:
        f.write(title_str+'\n')
        f.write(tag + ',' +
                date + ',' +
                str(open_price) + ',' +
                str(high) + ',' +
                str(low) + ',' +
                str(close) + ',' +
                str(volume) + '\n')


def write_one_row(row):
    data = row[1]
    title_str = 'tag,date,open,high,low,close,volume'
    tag = data[0]
    date = data['date'].strftime('%Y-%m-%d')
    open_price = data['open']
    high = data['high']
    low = data['low']
    close = data['close']
    volume = data['volume']
    with open(os.getenv('DATA_PATH') + '/' + tag + '.' + date, 'w') as f:
        f.write(title_str + '\n' +
                tag + ',' +
                date + ',' +
                str(open_price) + ',' +
                str(high) + ',' +
                str(low) + ',' +
                str(close) + ',' +
                str(volume) + '\n')


def deal_history_data(history_data, start_dt, end_dt):
    filtered = history_data[(history_data.date >= start_dt) &
                            (history_data.date <= end_dt)]
    for row in filtered.iterrows():
        write_one_row(row)


if __name__ == '__main__':
    argv = sys.argv
    tag1 = 'SH000300'
    tag2 = 'CHAU'
    today = time.strftime('%Y-%m-%d', time.localtime())
    deal_his = argv[1] if len(argv) >= 2 else 'today'
    start_dt = argv[2] if len(argv) >= 3 else time.strftime('%Y-%m-%d')
    end_dt = argv[3] if len(argv) >= 4 else time.strftime('%Y-%m-%d')
    if deal_his == 'today':
        while True:
            if int(time.strftime('%H', time.localtime())) > 20:
                break
            df = utils.get_history_data(tag1)
            dt = df[-1:].iloc[0]['date'].strftime('%Y-%m-%d')
            if dt != today:
                print('sleep')
                time.sleep(60)
                continue
            else:
                today_data = df[-1:]
                deal_data(today_data)
                break
    elif deal_his == 'history':
        df = utils.get_history_data(tag1)
        deal_history_data(df, start_dt, end_dt)
    else:
        print(argv[1] + 'error')
        sys.exit(1)
