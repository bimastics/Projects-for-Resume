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
        self.file = 'database.csv'

        with open(self.file, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            self.id_to_csv = [int(row['id']) for row in reader]
            self.column_name = reader.fieldnames

    def process_item(self, item, spider):
        csv_file = open(self.file, 'a', newline='', encoding='UTF-8')
        colums = item.fields.keys()

        data = csv.DictWriter(csv_file, colums)
        if not self.column_name:
            data.writeheader()
            self.column_name = True

        if item['id'] not in self.id_to_csv:
            data.writerow(item)
        csv_file.close()

        return item
