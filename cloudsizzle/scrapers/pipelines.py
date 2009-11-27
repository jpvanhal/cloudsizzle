# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from cloudsizzle.scrapers.items import CourseItem
from kpwrapper import SIBConnection, Triple

class SIBPipeline(object):
    def __init__(self):
        self.sc = SIBConnection('SIB console', 'preconfigured')
        
    def __del__(self):
        self.sc.close()

    def process_item(self, domain, item):
        if isinstance(item, CourseItem):
            try:
                self.sc.insert(Triple(item['code'], 'rdf:type', 'Course'))
                self.sc.insert(Triple(item['code'], 'name', item['name']))
            except Exception, e:
                print(e)
        return item
