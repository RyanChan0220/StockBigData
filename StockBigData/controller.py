#coding=utf-8
__author__ = 'Administrator'

from StockBigData.Frameworks.dlTrans import DownloadTrans
from StockBigData.analysis import Analyzer
from StockBigData.DBCmd import *
import ConfigParser
from multiprocessing.dummy import Pool as ThreadPool
import time


# 1 PROCESS 	101.31
# 4 		17.54
# 7		13.14
# 8		7.93
# 9		12.05
# 10		8.34
# 16		15.48
fork_processing = 8

dt = DownloadTrans()
def download_excel(stock_ids):
    dt.download(stock_ids)


def analyzer_all():
    mysql = MySQL("trans")
    mysql.connect()
    tables = mysql.query_all_tables()
    for table in tables:
        analyzer = Analyzer(table[0])
        print "starting analyzing %s" % table[0]
        analyzer.run()


if __name__ == '__main__':
    # time1 = time.time()
    # cf = ConfigParser.ConfigParser()
    # cf.read("trans.conf")
    # stock_ids = cf.get("stocks", "ids").split(",")
    # pool = ThreadPool(fork_processing)
    # ret = pool.map(download_excel, stock_ids)
    # pool.close()
    # pool.join()
    # time2 = time.time()
    # print time2 - time1
    # download_excel()

    # daily2DB("C:\\new_gdzq_v6\\T0002\\export", "daily")
    # download_excel()
    trans_db_multi("trans", "D:\\StockData\\trans")
    # analyzer_all()

