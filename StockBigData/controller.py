#coding=utf-8
__author__ = 'Administrator'

from StockBigData.downloadTrans import DownloadTrans
from StockBigData.analysis import Analyzer
from StockBigData.trans2DB import *
from StockBigData.liteTools import *
from daily2DB import Daily2DB
import time


def download_excel():
    dt = DownloadTrans()
    dt.download_multi()


@decorator_run_time
def analyzer_all():
    analyzer = Analyzer()
    analyzer.run_multi()



if __name__ == '__main__':
    # time1 = time.time()

    # daily_handler = Daily2DB("daily", "C:\\new_gdzq_v6\\T0002\\export")
    # daily_handler.daily2conf()
    # daily_handler.daily2db_multi()
    # download_excel()
    # trans_handler = Trans2DB("trans", "D:\\StockData\\trans")
    # trans_handler.trans_db_multi()

    analyzer_all()
    # time2 = time.time()
    # print time2 - time1



