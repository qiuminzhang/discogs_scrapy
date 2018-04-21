# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging


# https://alysivji.github.io/mongodb-pipelines-in-scrapy.html
class MongoPipeline(object):

    collection_base = 'scrapy_'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        Methods decorated by @classmethod is not required a class instance to access the method.
        The difference between @classmethod and @staticmethod is that @classmethod can be called both by itself and
        the object because it works with the class, but staticmethod knows nothing about the class and just deal with
        the parameters.
        :param crawler: cls is class itself rather than object / instance.
        :return:
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    # This method is called when spider is opened
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # This method is called when spider is closed
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = self.collection_base + item['genre']
        print(item)
        self.db[collection_name].insert_one(dict(item))
        print('done')
        logging.debug('Post added to MongoDB')
        return item