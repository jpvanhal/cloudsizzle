# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from cloudsizzle.scrapers.items import CourseItem

class SIBPipeline(object):
    def process_item(self, domain, item):
        if isinstance(item, CourseItem):
            print(item['department']['code'])
            #print(item['faculty']['name'])
        print("TEST")
        return item
