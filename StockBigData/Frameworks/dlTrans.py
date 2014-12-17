__author__ = 'Administrator'

import ConfigParser
import urllib
import os
import datetime
import thread

mylock = thread.allocate_lock()

class DownloadTrans(object):
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("trans.conf")
        self.url_template = self.cf.get("global", "url_template")
        self.dst_dir = self.cf.get("global", "download_dir")
        if os.path.isdir(self.dst_dir):
            pass
        else:
            os.mkdir(self.dst_dir)

    @staticmethod
    def __cov_string2date(str_date):
        mylock.acquire()
        ret = datetime.datetime.strptime(str_date, "%Y-%m-%d")
        mylock.release()
        return ret

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
            urllib.urlretrieve(url, filename)
            if os.path.getsize(filename) < 2048:
                os.remove(filename)
                print "Empty file %s" % filename
            else:
                print "xls file write to %s" % filename





