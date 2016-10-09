#!/usr/bin/env python3
import time
import tushare as ts
from urllib import request

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
       + 'AppleWebKit/537.11 (KHTML, like Gecko) '
       + 'Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,'
       + 'application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def get_history_data(code, start_dt, end_dt):
    url = "http://xueqiu.com/S/" + code + "/historical.csv"
    req = request.Request(url, headers=hdr)
    page = request.urlopen(req)
    content = page.read()
    


if __name__ == '__main__':
    get_history_data("CHAD", "2016-10-01", "2016-10-10")
