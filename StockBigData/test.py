__author__ = 'Administrator'

import urllib
import time
from datetime import date
import datetime
import os


def cov_sec2date(sec):
    return time.ctime(sec)


if __name__ == '__main__':
    xls_url = 'http://market.finance.sina.com.cn/downxls.php?date=2014-01-01&symbol=sz300104'
    dir = '../../stockInfoCrawler//trans/'
    if os.path.isdir(dir):
        pass
    else:
        os.mkdir(dir)
    sec = time.time()
    today = date(2014, 7, 12)
    tom = datetime.datetime.strptime("2014-07-12", "%Y-%m-%d")
    print tom
    print today.isoweekday()
    print today.weekday()
    print today
    today = today.replace(day=today.day - 1)
    print today

    print time.localtime(sec)
    print time.gmtime(sec)
    print time.time()
    print cov_sec2date(sec)