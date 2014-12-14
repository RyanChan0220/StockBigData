__author__ = 'ryan'

from datetime import datetime
from datetime import timedelta
from stockInfoCrawler.Frameworks.MySQL import MySQL
import matplotlib.pyplot as plt
import numpy as np


class Analyzer(object):
    stock_name = "xx000000"

    def __init__(self, stock_name):
        self.stock_name = stock_name

    def run(self):
        start_date = datetime.strptime('2014-01-01;00:00:00', "%Y-%m-%d;%H:%M:%S")
        end_date = datetime.strptime('2014-12-10;23:59:59', "%Y-%m-%d;%H:%M:%S")
        # self.analysis_deal_price(stock_name, start_date, end_date, plt, 'r')
        self.analysis_close_price(self.stock_name, start_date, end_date, plt, 'b')
        # self.analy_big_trans(self.stock_name, 100000, start_date, end_date, plt, 'r')
        self.analy_deal_type(self.stock_name, start_date, end_date, plt, 'r')
        # plt.show()
        plt.clf()
        

    def analy_deal_type(self, stock_name, start_date, end_date, plt, color):
        delta_days = (end_date - start_date).days
        mysql = MySQL('trans')
        mysql.connect()
        for day in xrange(0, delta_days, 1):
            today = start_date + timedelta(days=day)
            next_day = start_date + timedelta(days=day+1)
            state_where_buy = "DEAL_DATE > '%s' and DEAL_DATE < '%s' and DEAL_TYPE = 1" % (today, next_day)
            buy_data = mysql.query_where(stock_name, state_where_buy)
            cnt_buy_data = len(buy_data)
            state_where_sell = "DEAL_DATE > '%s' and DEAL_DATE < '%s' and DEAL_TYPE = -1" % (today, next_day)
            sell_data = mysql.query_where(stock_name, state_where_sell)
            cnt_sell_data = len(sell_data)
            scale = 5
            if cnt_sell_data is not 0:
                if cnt_buy_data is not 0:
                    buy_total = self.sum_long(buy_data)
                else:
                    buy_total = 0
                sell_total = self.sum_long(sell_data)
                perc = (float(buy_total) / sell_total) * scale
                # perc = (float(cnt_buy_data) / cnt_sell_data) * scale
            else:
                perc = 0
            plt.scatter(today, perc, c=color)
        plt.axhline(y=scale, xmin=0, xmax=1)
        try:
            plt.savefig(".\\results\\"+self.stock_name+".png", dpi=200)
        except Exception:
            print "save png file error!"
        mysql.close_connect()

    def analy_big_trans(self, stock_name, gate_money, start_date, end_date, plt, color):
        delta_days = (end_date - start_date).days
        mysql = MySQL('trans')
        mysql.connect()
        for day in xrange(0, delta_days, 1):
            today = start_date + timedelta(days=day)
            next_day = start_date + timedelta(days=day+1)
            state_where = "DEAL_DATE > '%s' and DEAL_DATE < '%s' and TOTAL_AMOUNT > %d" % (today, next_day, gate_money)
            big_data = mysql.query_where(stock_name, state_where)
            state_where = "DEAL_DATE > '%s' and DEAL_DATE < '%s'" % (today, next_day)
            all_data = mysql.query_where(stock_name, state_where)
            cnt_big_data = len(big_data)
            cnt_all_data = len(all_data)
            if cnt_all_data is not 0:
                perc = (float(cnt_big_data) / cnt_all_data) * 100
            else:
                perc = 0
            plt.scatter(today, perc, c=color)
        mysql.close_connect()


    def analysis_close_price(self, stock_name, start_date, end_date, plt, color):
        one_day = timedelta(days=1)
        delta_days = (end_date - start_date).days
        mysql = MySQL('daily')
        mysql.connect()
        for day in xrange(0, delta_days, 1):
            query_day = start_date + timedelta(days=day)
            state_where = "DATE = '%s'" % query_day
            data = mysql.query_where(stock_name, state_where)
            if len(data) > 0:
                plt.scatter(query_day, data[0][5], c=color)
            else:
                plt.scatter(query_day, 0, c=color)
        mysql.close_connect()

    def analysis_deal_price(self, stock_name, start_date, end_date, plt, color):
        one_day = timedelta(days=1)
        delta_days = (end_date - start_date).days
        mysql = MySQL('trans')
        mysql.connect()
        for day in xrange(0, delta_days, 1):
            query_day = start_date + timedelta(days=day)
            state_where = "DEAL_DATE > '%s' and DEAL_DATE < '%s'" % (query_day, query_day + one_day)
            data = mysql.query_where(stock_name, state_where)
            ret = self.max_data(data)
            # ax.scatter(query_day, ret, c=color)
            plt.plot(query_day, ret, 'o-', c=color)
        mysql.close_connect()

    def show_data(self, data):
        prices = []
        for index in xrange(len(data)):
            prices.append(int(data[index][2] * 100))
        x_axis = {}
        for price in range(min(prices) - 1, max(prices) + 1, 1):
            x_axis[price] = 0
        for index in xrange(len(prices)):
            x_axis[prices[index]] += data[index][4]
        print x_axis
        fig = plt.figure()
        ax = fig.gca()

        for price in x_axis:
            ax.scatter(price, x_axis[price])
        plt.show()

    def mean_data(self, data):
        gate_amount = 100000
        day_total = 0
        lot_total = 0
        if len(data) > 0:
            for index in xrange(len(data)):
                if data[index][5] > gate_amount:
                    day_total += data[index][5]
                    lot_total += data[index][4]
            mean_total = day_total / lot_total
        else:
            mean_total = 0
        return mean_total / 100

    def max_data(self, data):
        max_amount = 0
        max_lot = 0
        max_price = 0
        if len(data) > 0:
            for index in xrange(len(data)):
                if data[index][5] > max_amount:
                    max_amount = data[index][5]
                    max_lot = data[index][4]
                    max_price = data[index][2]
        else:
            max_price = 0
        return max_price

    def sum_long(self, array):
        ret = 0
        for num in array:
            ret += num[5]
        return ret