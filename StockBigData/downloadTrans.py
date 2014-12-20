__author__ = 'Administrator'

import ConfigParser
import urllib
import os
import datetime
import thread
from multiprocessing.dummy import Pool as ThreadPool

# 1 PROCESS 	101.31
# 4 		17.54
# 7		13.14
# 8		7.93
# 9		12.05
# 10		8.34
# 16		15.48
fork_processing = 8
my_lock = thread.allocate_lock()


class DownloadTrans(object):
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("trans.conf")
        self.url_template = self.cf.get("global", "url_template")
        self.dst_dir = self.cf.get("global", "download_dir")
        self.stock_ids = self.cf.get("stocks", "ids").split(",")
        if os.path.isdir(self.dst_dir):
            pass
        else:
            os.mkdir(self.dst_dir)

    @staticmethod
    def __cov_string2date(str_date):
        my_lock.acquire()
        ret = datetime.datetime.strptime(str_date, "%Y-%m-%d")
        my_lock.release()
        return ret

    def download_multi(self):
        pool = ThreadPool(fork_processing)
        ret = pool.map(self.download, self.stock_ids)
        pool.close()
        pool.join()

    def download(self, stock_id):
        start = self.cf.get(stock_id, "start")
        end = self.cf.get(stock_id, "end")
        d_start = self.__cov_string2date(start)
        d_end = self.__cov_string2date(end)
        days = []
        while d_start <= d_end:
            if d_start.isoweekday() <= 5:
                days.append(d_start.strftime("%Y-%m-%d"))
            else:
                pass
            d_start = d_start + datetime.timedelta(days=1)
        file_dir = self.dst_dir + stock_id
        if os.path.isdir(file_dir):
            pass
        else:
            os.mkdir(file_dir)
        for day in days:
            url = self.url_template + "date=%s&symbol=%s" % (day, stock_id)
            filename = file_dir + '/' + day + '.txt'
            try:
                urllib.urlretrieve(url, filename)
                if os.path.getsize(filename) < 2048:
                    os.remove(filename)
                    print "Empty file %s" % filename
                else:
                    print "xls file write to %s" % filename
            except IOError, e:
                print "download %s failed, connect error!" % url






