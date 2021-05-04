from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avitoparse import settings
from avitoparse.spiders.avito_real_estate import AvitoRealEstateSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AvitoRealEstateSpider)
    crawler_process.start()
