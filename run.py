#!/usr/bin/env python3
import utils
import time
import os

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
    with open(os.getenv('DATA_PATH') + '/' + date + '/' + tag, 'w') as f:
        f.write(title_str+'\n')
        f.write(tag + ',' +
                date + ',' +
                str(open_price) + ',' +
                str(high) + ',' +
                str(low) + ',' +
                str(close) + ',' +
                str(volume) + '\n')


if __name__ == '__main__':
    tag1 = 'SH000300'
    tag2 = 'CHAU'
    today = time.strftime('%Y-%m-%d', time.localtime())
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
            deal_data(today_data, today)
            break
