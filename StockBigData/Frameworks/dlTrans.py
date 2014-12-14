__author__ = 'Administrator'

import ConfigParser
import urllib
import os
import datetime


class DownloadTrans(object):
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("trans.conf")
        self.stocks_id = self.cf.get("stocks", "ids").split(",")
        self.url_template = self.cf.get("global", "url_template")
        self.dst_dir = self.cf.get("global", "download_dir")
        if os.path.isdir(self.dst_dir):
            pass
        else:
            os.mkdir(self.dst_dir)

    @staticmethod
    def __cov_string2date(str_date):
        return datetime.datetime.strptime(str_date, "%Y-%m-%d")

    def download(self):
        for stock in self.stocks_id:
            start = self.cf.get(stock, "start")
            end = self.cf.get(stock, "end")
            d_start = self.__cov_string2date(start)
            d_end = self.__cov_string2date(end)
            days = []
            while d_start <= d_end:
                if d_start.isoweekday() <= 5:
                    days.append(d_start.strftime("%Y-%m-%d"))
                else:
                    pass
                d_start = d_start + datetime.timedelta(days=1)
            file_dir = self.dst_dir + stock
            if os.path.isdir(file_dir):
                pass
            else:
                os.mkdir(file_dir)
            for day in days:
                url = self.url_template + "date=%s&symbol=%s" % (day, stock)
                filename = file_dir + '/' + day + '.txt'
                urllib.urlretrieve(url, filename)
                if os.path.getsize(filename) < 2048:
                    os.remove(filename)
                    print "Empty file %s" % filename
                else:
                    print "xls file write to %s" % filename





