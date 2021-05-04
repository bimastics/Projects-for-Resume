import scrapy


class AvitoRealEstateSpider(scrapy.Spider):
    name = 'avito_real_estate'
    allowed_domains = ['avito.ru']
    start_urls = ['http://avito.ru/']

    def parse(self, response):
        pass
