# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiscoverlifeItem(scrapy.Item):
    # define the fields for your item here like:
    biological_name = scrapy.Field()
    common_name = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    date = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    url = scrapy.Field()
