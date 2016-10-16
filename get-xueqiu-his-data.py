#!/usr/bin/env python3
from urllib import request
import pandas as pd
import io
import numpy as np

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
       + 'AppleWebKit/537.11 (KHTML, like Gecko) '
       + 'Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,'
       + 'application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def get_history_data(code):
    url = "http://xueqiu.com/S/" + code + "/historical.csv"
    req = request.Request(url, headers=hdr)
    page = request.urlopen(req)
    content = page.read()
    df = pd.read_csv(io.BytesIO(content), encoding='utf-8', parse_dates=[1])
    return df


def get_data_by_date(df, dt):
    return df.assign(date=dt)


def calc_row_data(tag, df):
    df[tag + '-diff-price'] = df['close'] - df['open']
    df[tag + '-diff-price-rate'] = df[tag + '-diff-price'] / df['open']
    df[tag + '-max-diff-price'] = df['high'] - df['low']
    df.rename(columns={'open': tag + '-open',
                       'high': tag + '-high',
                       'low': tag + '-low',
                       'close': tag + '-close',
                       'volume': tag + '-volume'},
              inplace=True)
    return df


def up_up_down_down(row, tag1, tag2):
    if row[tag1 + '-diff-price'] > 0 and row[tag2 + '-diff-price'] > 0:
        return True
    elif row[tag1 + '-diff-price'] < 0 and row[tag2 + '-diff-price'] < 0:
        return True
    elif row[tag1 + '-diff-price'] == 0 or row[tag2 + '-diff-price'] == 0:
        return None
    else:
        return False


def calc_income(row, tag):
    if row['right'] is True:
        return np.abs(row[tag + '-diff-price'])
    elif row['right'] is False:
        return np.negative(np.abs(row[tag + '-diff-price']))
    elif row['right'] is None:
        return 0


def get_re_data(tag1, tag2, dt1, dt2=None):
    hs300 = get_history_data(tag1)
    chau = get_history_data(tag2)
    calc_row_data(tag1, hs300)
    calc_row_data(tag2, chau)
    merge_data = pd.merge(hs300, chau, on='date')
    merge_data['right'] = merge_data.apply(lambda row:
                                           up_up_down_down(row, tag1, tag2),
                                           axis=1)
    merge_data['income'] = merge_data.apply(lambda row:
                                            calc_income(row, tag2),
                                            axis=1)
    if dt2 is not None:
        return merge_data[(merge_data['date'] >= pd.tslib.Timestamp(dt1)) &
                          (merge_data['date'] < pd.tslib.Timestamp(dt2))]
    else:
        return merge_data[merge_data['date'] >= pd.tslib.Timestamp(dt1)]


def calc_re_data(tag, df):
    return None


if __name__ == '__main__':
    tag1 = 'SH000300'
    tag2 = 'CHAU'
    re = get_re_data(tag1, tag2, '2016-08-01')
