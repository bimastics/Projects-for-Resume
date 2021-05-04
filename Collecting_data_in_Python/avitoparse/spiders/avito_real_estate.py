import scrapy


class AvitoRealEstateSpider(scrapy.Spider):
    name = 'avito_real_estate'
    allowed_domains = ['www.avito.ru', 'avito.ru']
    start_urls = ['https://www.avito.ru/abakan/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1']

    def parse(self, response):
        for num in response.xpath('//div[@data-marker="pagination-button"]//span/text()'):
            try:
                tmp = int(num.get())
                yield response.follow(f'https://www.avito.ru/abakan/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p={tmp}', callback=self.parse)
            except ValueError as e:
                continue
