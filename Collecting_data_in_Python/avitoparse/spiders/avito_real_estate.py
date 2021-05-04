import scrapy
from scrapy.loader import ItemLoader
from avitoparse.items import AvitoRealEstateItem


class AvitoRealEstateSpider(scrapy.Spider):
    name = 'avito_real_estate'
    allowed_domains = ['www.avito.ru', 'avito.ru']
    start_urls = ['https://www.avito.ru/abakan/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1']

    # Page pagination
    def parse(self, response):
        for num in response.xpath('//div[@data-marker="pagination-button"]//span/text()'):
            try:
                tmp = int(num.get())
                yield response.follow(f'https://www.avito.ru/abakan/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p={tmp}',
                                      callback=self.parse)
            except ValueError as e:
                continue
            except TypeError as e:
                continue

        # Getting links of apartments
        for abs_url in response.xpath('//div[@data-marker="item"]//a//@href'):
            yield response.follow(abs_url, callback=self.abs_parse)

    def abs_parse(self, response):
        item = ItemLoader(AvitoRealEstateItem(), response)
        item.add_xpath('photos', "//div[contains(@class, 'gallery-img-frame')]/@data-url")
        yield item.load_item()
