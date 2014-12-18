__author__ = 'ryan'
import os
import ConfigParser
from os.path import join
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
from StockBigData.Frameworks.MySQL import MySQL
import thread

fork_processing = 1


class Daily2DB(object):
    my_lock = thread.allocate_lock()
    db_name = "daily"
    path = "C:\\new_gdzq_v6\\T0002\\export"

    def __init__(self, daily_db, src_dir):
        self.db_name = daily_db
        self.path = src_dir

    def daily2conf(self):
        start_date = '2014-01-01'
        end_date = '2014-12-11'
        cf = ConfigParser.ConfigParser()
        cf.add_section("api")
        cf.set("api", "daily_trans", "http://market.finance.sina.com.cn/downxls.php?date=2014-01-01&symbol=sz002410")
        cf.set("api", "daily_total", "http://hq.sinajs.cn/list=sh601006")
        cf.add_section("global")
        cf.set("global", "url_template", "http://market.finance.sina.com.cn/downxls.php?")
        cf.set("global", "download_dir", "D:/StockData/trans/")
        file_list = []
        for root1, dirs1, files1 in os.walk(self.path):
            for file_name in files1:
                file_name = file_name.lower()
                file_list.append(file_name.split(".")[0])
        cf.add_section("stocks")
        all_file = ''
        for file_name in file_list:
            cf.add_section(file_name)
            cf.set(file_name, "start", start_date)
            cf.set(file_name, "end", end_date)
            if file_name == file_list[len(file_list) - 1]:
                all_file += file_name
            else:
                all_file += file_name + ","
        cf.set("stocks", "ids", all_file)
        with open('trans.conf', 'wb') as fp:
            cf.write(fp)
            fp.close()

    def daily2db_multi(self):
        pool = ThreadPool(fork_processing)
        try:
            for root, dirs, files in os.walk(self.path):
                files_low = []
                for file_name in files:
                    files_low.append(file_name.lower())
                ret = pool.map(self.daily_file2db, files_low)
        except Exception, e:
            print e
        finally:
            pool.close()
            pool.join()

    def daily_file2db(self, stock_name):
        mysql = MySQL(self.db_name)
        mysql.connect()
        if stock_name.find('.txt') == -1:
            print "%s is error file!" % stock_name
        else:
            try:
                table_name = stock_name.split('.')[0]
                full_file_name = join(self.path, stock_name)
                txt_file = open(full_file_name)
                stock_name = txt_file.readline().decode('gbk').encode('utf-8')
                # for str in stock_name.split(" ", 3):
                # print str.lstrip().rstrip()
                title = txt_file.readline().decode('gbk').encode('utf-8')
                # for str in title.lstrip().split("\t", 7):
                #    print str.lstrip()
                print "Processing daily to DB File: %s" % stock_name.lstrip().rstrip()
                col_type = list()
                col_type.append("`ID` INT NOT NULL AUTO_INCREMENT")
                col_type.append("`DATE` DATETIME NULL")
                col_type.append("`START_PRICE` FLOAT NULL")
                col_type.append("`HIGH_PRICE` FLOAT NULL")
                col_type.append("`LOW_PRICE` FLOAT NULL")
                col_type.append("`CLOSE_PRICE` FLOAT NULL")
                col_type.append("`DEAL_AMOUNT` INT NULL")
                col_type.append("`DEAL_PRICE` FLOAT NULL")
                mysql.create_table_with_delete(table_name, "ID", col_type)
                content = txt_file.readline()
                data = list()
                while content:
                    content = content.replace('\n', '')
                    contents = content.split(';', 7)
                    content = txt_file.readline()
                    if len(contents) < 7:
                        continue
                    else:
                        self.my_lock.acquire()
                        contents[0] = datetime.strptime(contents[0], "%m/%d/%Y").strftime("%Y-%m-%d %H:%M:%S")
                        self.my_lock.release()
                        data.append(contents)
                mysql.insert_many(table_name, "`DATE`, `START_PRICE`, `HIGH_PRICE`, `LOW_PRICE`, \
                `CLOSE_PRICE`, `DEAL_AMOUNT`, `DEAL_PRICE`", data)
            except IOError, e:
                print "ERROR: " + e + "\tFile:" + stock_name
                raise e
        mysql.close_connect()


