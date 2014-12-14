#coding=utf-8
__author__ = 'ryan'

from stockInfoCrawler.Frameworks.MySQL import MySQL
from stockInfoCrawler.Frameworks.Excel import Excel
from datetime import datetime
import os
from os.path import join


def daily2DB(src, db_name):
    tables = []
    for root, dirs, files in os.walk(src):
        for file_name in files:
            if file_name.find('.txt') == -1:
                continue
            else:
                print "Processing daily to DB File: %s" % file_name
                table_name = file_name.split('.')[0]
                tables.append(table_name)
                full_file_name = join(root, file_name)
                txt_file = open(full_file_name)
                stock_name = txt_file.readline().decode('gbk').encode('utf-8')
                #for str in stock_name.split(" ", 3):
                #    print str.lstrip().rstrip()
                title = txt_file.readline().decode('gbk').encode('utf-8')
                #for str in title.lstrip().split("\t", 7):
                #    print str.lstrip()
                mysql = MySQL(db_name)
                mysql.connect()
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
                        contents[0] = datetime.strptime(contents[0], "%m/%d/%Y").strftime("%Y-%m-%d %H:%M:%S")
                        data.append(contents)
                mysql.insert_many(table_name, "`DATE`, `START_PRICE`, `HIGH_PRICE`, `LOW_PRICE`, \
                `CLOSE_PRICE`, `DEAL_AMOUNT`, `DEAL_PRICE`", data)
                mysql.close_connect()


def trans2db(db_name, trans_path):
    mysql = MySQL(db_name)
    mysql.connect()
    col_type = list()
    col_type.append("`ID` INT NOT NULL AUTO_INCREMENT")
    col_type.append("`DEAL_DATE` DATETIME NULL")
    col_type.append("`DEAL_PRICE` FLOAT NULL")
    col_type.append("`DEAL_GAP` FLOAT NULL")
    col_type.append("`TOTAL_LOT` INT NULL")
    col_type.append("`TOTAL_AMOUNT` INT NULL")
    col_type.append("`DEAL_TYPE` INT NULL")
    col_type.append("`OTHER` FLOAT NULL")
    try:
        for root1, dirs1, files1 in os.walk(trans_path):
            for dir1 in dirs1:
                mysql.create_table(dir1, "ID", col_type)
                next_dir = root1 + "\\" + dir1
                for root2, dirs2, files2 in os.walk(next_dir):
                    for file2 in files2:
                        if file2.find('.txt') != -1:
                            data = list()
                            file_path = join(next_dir, file2)
                            file_name = file2.split(".")[0]
                            with open(file_path, 'r') as fp:
                                text_list = fp.readlines()
                                print "Processing file to DB.... " + file_path
                                for i in range(1, len(text_list)):
                                    text = text_list[i].decode('gb2312').encode('utf-8')
                                    text_elem = text.split("\t")
                                    deal_time_str = file_name + ';' + text_elem[0].strip()
                                    check_ret = check_data(text_elem)
                                    if check_ret != 0:
                                        print "###########" + str(check_ret)
                                        if check_ret != 7:
                                            print text_elem[check_ret - 1]
                                        continue
                                    deal_time = datetime.strptime('1900-01-01;00:00:00', "%Y-%m-%d;%H:%M:%S")
                                    try:
                                        deal_time = datetime.strptime(deal_time_str, "%Y-%m-%d;%H:%M:%S")
                                    except Exception:
                                        print deal_time_str
                                    #deal nums
                                    deal_price = 0
                                    deal_gap = 0
                                    deal_lot = 0
                                    deal_amount = 0
                                    try:
                                        deal_price_str = text_elem[1].strip()
                                        deal_gap_str = text_elem[2].strip()
                                        deal_lot_str = text_elem[3].strip()
                                        deal_amount_str = text_elem[4].strip()

                                        deal_price = float(deal_price_str)
                                        if deal_gap_str.find('-') == -1:
                                            deal_gap = float(deal_gap_str)
                                        else:
                                            deal_gap = 0
                                        deal_lot = float(deal_lot_str)
                                        deal_amount = float(deal_amount_str)
                                    except Exception, e:
                                        print e
                                        print deal_price_str
                                        print deal_gap_str
                                        print deal_lot
                                        print deal_amount

                                    deal_type_str = text_elem[5].strip()
                                    deal_type = 0
                                    if deal_type_str == "买盘":
                                        deal_type = 1
                                    elif deal_type_str == "卖盘":
                                        deal_type = -1
                                    else:
                                        deal_type = 0

                                    if i == 1:
                                        ret = mysql.query(dir1, "DEAL_DATE", deal_time)
                                        if len(ret) > 0:
                                            print "pass this file!"
                                            break
                                        else:
                                            pass
                                    else:
                                        pass
                                    data.append([deal_time, deal_price, deal_gap, deal_lot, deal_amount, deal_type])
                            if len(data) > 0:
                                mysql.insert_many(dir1, "`DEAL_DATE`, `DEAL_PRICE`, `DEAL_GAP`, \
                                    `TOTAL_LOT`, `TOTAL_AMOUNT`, `DEAL_TYPE`", data)
                            else:
                                pass
                            fp.close()
                            os.remove(file_path)
                        else:
                            continue
                os.rmdir(next_dir)
    except IOError, e:
        print "ERROR: " + dir1 + " FILE: " + file2
        mysql.close_connect()
    mysql.close_connect()


def check_data(data):
    if len(data) == 6:
        if len(data[0]) > 10:
            ret = 1
        elif len(data[1]) > 10:
            ret = 2
        elif len(data[2]) > 10:
            ret = 3
        elif len(data[3]) > 20:
            ret = 4
        elif len(data[4]) > 20:
            ret = 5
        elif len(data[5]) > 10:
            ret = 6
        else:
            ret = 0
    else:
        ret = 7
    return ret
