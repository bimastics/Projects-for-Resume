# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class AvitoparseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class AvitoRealEstateItem(scrapy.Item):
    id = scrapy.Field(input_processor=MapCompose(lambda data: int(data[2:])), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()

    house_type = scrapy.Field(output_processor=TakeFirst())
    house_floor = scrapy.Field(output_processor=TakeFirst())
    floor = scrapy.Field(output_processor=TakeFirst())
    rooms = scrapy.Field(output_processor=TakeFirst())
    total_square = scrapy.Field(output_processor=TakeFirst())
    active_square = scrapy.Field(output_processor=TakeFirst())
    kitchen_square = scrapy.Field(output_processor=TakeFirst())
    balcony_or_loggia = scrapy.Field(output_processor=TakeFirst())
    view_from_window = scrapy.Field(output_processor=TakeFirst())
