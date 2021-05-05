# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import scrapy
import csv
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class AvitoparsePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.avito_photo_312

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        if item.get('photos'):
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results]
        return item


class CSVPipeline(object):
    def __init__(self):
        self.file = f'database.csv'
        with open(self.file, 'r', newline='') as csv_file:
            self.tmp_data = csv.DictReader(csv_file).fieldnames

        self.csv_file = open(self.file, 'a', newline='', encoding='UTF-8')

    def process_item(self, item, spider):
        colums = item.fields.keys()

        data = csv.DictWriter(self.csv_file, colums)
        if not self.tmp_data:
            data.writeheader()
            self.tmp_data = True
        data.writerow(item)
        return item

    def __del__(self):
        self.csv_file.close()
