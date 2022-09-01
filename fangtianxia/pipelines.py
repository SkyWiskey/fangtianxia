# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from .items import NewhouseItem,EsfItem

class FangtianxiaPipeline:
    def __init__(self):
        self.MongoClient = pymongo.MongoClient('127.0.0.1',27017)
        self.new_house_collection = self.MongoClient['Fangtianxia']['NewHouse']
        self.esf_house_collection = self.MongoClient['Fangtianxia']['EsfHouse']

    def open_spider(self,spider):
        print('房天下房源信息采集开始咯')

    def process_item(self, item, spider):
        if isinstance(item,NewhouseItem):
            self.new_house_collection.insert_one(dict(item))
        else:
            self.esf_house_collection.insert_one(dict(item))
        return item

    def close_spider(self,spider):
        self.MongoClient.close()
        print('房源信息采集完成，爬虫结束')

