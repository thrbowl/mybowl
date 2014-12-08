# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    keywords = scrapy.Field()
    tags = scrapy.Field()
    categories = scrapy.Field()
    refer_url = scrapy.Field()

    def __str__(self):
        return self.refer_url
