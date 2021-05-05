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
        for abs_url in response.xpath('//div[@data-marker="item"]/div/div/a//@href'):
            yield response.follow(abs_url, callback=self.abs_parse)

    def abs_parse(self, response):
        item = ItemLoader(AvitoRealEstateItem(), response)
        item.add_css('id', 'div.item-view-search-info-redesign span::text')
        item.add_value('url', response.url)
        item.add_css('title', 'div.title-info-main h1.title-info-title span::text')
        item.add_xpath('photos', "//div[contains(@class, 'gallery-img-frame')]/@data-url")

        house_data = response.css("div.item-params ul li")

        for param in house_data:
            info = param.css("::text").extract()

            if 'Тип дома' in info[1]:
                item.add_value('house_type', info[-1].strip())
            elif 'Этаж' in info[1]:
                item.add_value('floor', int(info[-1][0]))
                item.add_value('house_floor', int(info[-1][-2]))
            elif 'Количество комнат' in info[1]:
                item.add_value('rooms', int(info[-1].strip()))
            elif 'Общая площадь' in info[1]:
                item.add_value('total_square', float(info[-1][:-4]))
            elif 'Балкон' in info[1]:
                item.add_value('balcony_or_loggia', info[-1].strip())
            elif 'Вид из окна' in info[1]:
                item.add_value('view_from_window', info[-1])
            elif 'Жилая площадь' in info[1]:
                item.add_value('active_square', float(info[-1][:-4]))
            elif 'Площадь кухни' in info[1]:
                item.add_value('kitchen_square', float(info[-1][:-4]))

        yield item.load_item()
