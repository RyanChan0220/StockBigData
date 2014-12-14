#coding=utf-8
__author__ = 'Administrator'

from StockBigData.Frameworks.dlTrans import DownloadTrans
from StockBigData.analysis import Analyzer
from StockBigData.DBCmd import *


def download_excel():
    dt = DownloadTrans()
    dt.download()


def analyzer_all():
    mysql = MySQL("trans")
    mysql.connect()
    tables = mysql.query_all_tables()
    for table in tables:
        analyzer = Analyzer(table[0])
        print "starting analyzing %s" % table[0]
        analyzer.run()


if __name__ == '__main__':
    # daily2DB("C:\\new_gdzq_v6\\T0002\\export", "daily")
    download_excel()
    trans2db("trans", "D:\\StockData\\trans")
    analyzer_all()



