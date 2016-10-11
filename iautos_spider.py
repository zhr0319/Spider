# -*- coding: utf-8 -*-
import sys
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
import scrapy
import datetime


class IautosSpider(scrapy.Spider):
    name = 'iautos.com'

    start_urls = [
        'http://so.iautos.cn/fuzhou/pas2dsvepcatcpbnscac/', 
        'http://so.iautos.cn/shanghai/pas2dsvepcatcpbnscac/', 
        'http://so.iautos.cn/xiamen/pas2dsvepcatcpbnscac/'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2.0,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }

    def parse(self, response):
        for car in response.css('div.principal-graphs > ul > li'):
            yield scrapy.Request(car.css('a::attr(href)').extract_first().strip(), callback=self.parse_details)

        yield scrapy.Request(response.urljoin(response.css('div.principal-pages-wrap > .side.mr::attr(href)').extract_first()), callback=self.parse)


    def parse_details(self, response):
        data = {
            'url': response.url,
            'city': response.css('meta[name="location"]::attr(content)').extract_first().split(';')[1].split('=')[-1],
            'dateline': datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'tel': response.css('#show-contect-phone > span::text').extract_first(),
            'title': response.css('h2.title.de-drei-col > span::text').extract_first().strip(),
            'price': ''.join(response.css('.price.clean > .price-l > span ::text').extract()),
            'mileage': response.css('.de-left-bord > p::text').extract_first(),
            'location': response.css('div.address > span.de-drei-col > i::text').extract_first(),
            'license_date': response.css('.d.de-drei-col::text').extract_first(),
            'description': response.css('meta[name="description"]::attr(content)').extract_first(),
        }

        yield data
