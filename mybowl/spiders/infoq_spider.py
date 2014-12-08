# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request

from ..items import ArticleItem


class IbmSpider(CrawlSpider):
    name = 'infoq'
    allowed_domains = ['infoq.com']
    start_urls = [
        'http://www.infoq.com/cn/articles',
    ]

    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//div[contains(@class, "news_type2")]/h2',)),
             callback='parse_items', follow=False),
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="blue"]',)),callback='parse_urls', follow=True)
    ]

    def parse_urls(self, response):
        extractor = LinkExtractor(restrict_xpaths=('//div[contains(@class, "news_type2")]/h2',))
        links = extractor.extract_links(response)
        for link in links:
            url = link.url
            yield Request(url, callback=self.parse_items)

    def parse_items(self, response):
        sel = Selector(response)
        article = ArticleItem()
        article['title'] = sel.xpath('//div[@id="content"]/h1/text()')[0].extract()
        article['content'] = sel.xpath('//div[@class="text_info text_info_article"]')[0].extract()
        article['refer_url'] = response.url
        return article

    def clean_content(self):
        pass
