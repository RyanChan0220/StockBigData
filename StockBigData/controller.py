#coding=utf-8
__author__ = 'Administrator'

from StockBigData.Frameworks.dlTrans import DownloadTrans
from StockBigData.analysis import Analyzer
from StockBigData.DBCmd import *
import ConfigParser
from multiprocessing.dummy import Pool as ThreadPool


fork_processing = 2


def download_excel(stock_ids):
    dt = DownloadTrans(stock_ids)
    dt.download()


def analyzer_all():
    mysql = MySQL("trans")
    mysql.connect()
    tables = mysql.query_all_tables()
    for table in tables:
        analyzer = Analyzer(table[0])
        print "starting analyzing %s" % table[0]
        analyzer.run()

def print_cnt(num):
    for i in xrange(num):
        print "The CNT IS %d" % i


if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    cf.read("trans.conf")
    stock_ids = cf.get("stocks", "ids").split(",")
    stocks_len = len(stock_ids)
    piece_len = stocks_len / fork_processing
    piece_ids = list()
    for cnt in xrange(fork_processing):
        if cnt == fork_processing-1:
            piece_ids.append(stock_ids[cnt * piece_len:])
        else:
            piece_ids.append(stock_ids[cnt*piece_len:(cnt+1)*piece_len])
    pool = ThreadPool(fork_processing)
    list1 = [['sh600701'], ['sh600702']]
    list2 = ['sh600702']
    ret = pool.map(download_excel, list1)
    pool.close()
    pool.join()
    # download_excel()

    # daily2DB("C:\\new_gdzq_v6\\T0002\\export", "daily")
    # download_excel()
    # trans2db("trans", "D:\\StockData\\trans")
    # analyzer_all()



