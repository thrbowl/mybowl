# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request

from ..items import ArticleItem


class IbmSpider(CrawlSpider):
    name = 'ibm'
    allowed_domains = ['ibm.com']
    start_urls = [
        'https://www.ibm.com/developerworks/cn/views/web/libraryview.jsp?type_by=%E6%8A%80%E6%9C%AF%E6%96%87%E7%AB%A0',
    ]

    rules = [
        Rule(LinkExtractor(restrict_xpaths=('table[contains(@class,ibm-data-table)]/tbody',)),
                  callback='parse_urls', follow=False),
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="ibm-forward-em-link"]',)),
                  callback='parse_urls', follow=False)
    ]

    def parse_urls(self, response):
        extractor = LinkExtractor(restrict_xpaths=('//table[contains(@class,ibm-data-table)]/tbody',))
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
