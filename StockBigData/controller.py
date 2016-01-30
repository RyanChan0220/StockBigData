# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from StockBigData.downloadTrans import DownloadTrans
from StockBigData.analysis import Analyzer
from StockBigData.analysis import TrendAnalyzer
from StockBigData.analysis import LeastSquareMethod
from StockBigData.trans2DB import *
from StockBigData.liteTools import *
from daily2DB import Daily2DB
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime


def download_excel():
    dt = DownloadTrans()
    dt.download_multi()


@decorator_run_time
def analyzer_all():
    analyzer = Analyzer()
    analyzer.run_multi()


def file2DB():
    daily_handler = Daily2DB("daily", "C:\\new_gdzq_v6\\T0002\\export")
    daily_handler.daily2conf()
    daily_handler.daily2db_multi()


def trend_analysis():
    analysis = TrendAnalyzer("daily")
    allP = analysis.get_table_all_point("sh600005")
    allP_datas = TrendAnalyzer.cov_datetime2num(allP.keys())
    max_min = analysis.get_table_all_maxmin_point("sh600005")
    dates = TrendAnalyzer.cov_datetime2num(max_min.keys())
    stock_date = np.array(dates)
    stock_price = np.array(max_min.values())

    # print stock_date
    # print stock_price
    new_date = TrendAnalyzer.cov_arrayone(stock_date, 7)
    new_price = TrendAnalyzer.cov_arrayone(stock_price, 7)
    print new_date.ndim, new_date.shape, new_date
    plt.subplot(3, 1, 1)
    plt.plot(np.array(allP_datas), np.array(allP.values()))
    plt.subplot(3, 1, 2)
    plt.plot(stock_date, stock_price, '.')
    tmp = []
    plt.subplot(3, 1, 3)
    for cnt in xrange(new_date.shape[0]):
        analysis = LeastSquareMethod(new_date[cnt], new_price[cnt])
        para = analysis.runLSM()
        tmp.append(para[0][0])
        # print para
        x1 = new_date[cnt][new_date.shape[1]-1]
        x2 = new_date[cnt][new_date.shape[1] - 1]
        y1 = para[0][0]*x1+para[0][1]
        y2 = para[0][0]*x2+para[0][1]

        plt.plot(x1, para[0][0], '*')
        # print [x1, x2], [y1, y2]
        # plt.plot([x1, x2], [y1, y2])
    print tmp
    plt.show()

if __name__ == '__main__':
    # time1 = time.time()
    # download_excel()
    # trans_handler = Trans2DB("trans", "D:\\StockData\\trans")
    # trans_handler.trans_db_multi()

    # analyzer_all()
    # time2 = time.time()
    # print time2 - time1
    trend_analysis()






