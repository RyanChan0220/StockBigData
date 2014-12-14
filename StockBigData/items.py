# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class TestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    sell_5 = Field()
    sell_4 = Field()
    sell_3 = Field()
    sell_2 = Field()
    sell_1 = Field()
    deal = Field()
    buy_1 = Field()
    buy_2 = Field()
    buy_3 = Field()
    buy_4 = Field()
    buy_5 = Field()