__author__ = 'Administrator'

from scrapy.spider import Spider
import time


class StockSpider(Spider):
    name = "Stock"
    allowed_domains = ["http://finance.sina.com.cn/"]
    start_urls = [
        "http://finance.sina.com.cn/realstock/company/sz300104/nc.shtml"
    ]

    def parse(self, response):
        filename = time.time().__str__() + response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)