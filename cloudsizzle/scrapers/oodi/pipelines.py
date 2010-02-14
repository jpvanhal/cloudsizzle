# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from cloudsizzle.scrapers.items import CompletedCourseItem, ModuleItem
from cloudsizzle.kp import SIBConnection, Triple, literal, uri, bnode
from scrapy.conf import settings

class SIBPipeline(object):
    def __init__(self):
        self.asi_user_id = settings['ASI_USER_ID']
        if not self.asi_user_id:
            self.asi_user_id = raw_input('ASI User ID: ')

        self.sc = SIBConnection(method='preconfigured')
        self.sc.open()

    def __del__(self):
        self.sc.close()

    def transform_to_triples(self, item):
        if isinstance(item, CompletedCourseItem):
            namespace = 'http://cloudsizzle.cs.hut.fi/ontology/'
            uri = '{0}people/{1}/courses/completed/{2}'.format(
                namespace, self.asi_user_id, item['code'])
            return [
                Triple(uri, 'rdf:type', 'CompletedCourse'),
                Triple(uri, 'user_id', self.asi_user_id),
                Triple(uri, 'code', item['code']),
                Triple(uri, 'name', item['name']),
                Triple(uri, 'cr', item['cr']),
                Triple(uri, 'ocr', item['ocr']),
                Triple(uri, 'grade', item['grade']),
                Triple(uri, 'date', item['date'].isoformat()),
                Triple(uri, 'teacher', item['teacher'])]
        # TODO: module is missing
        # elif isinstance(item,ModuleItem):
        #    return [
        #        Triple(item['code'], 'rdf:type', 'Module'),
        #        Triple(item['code'], 'name', item['name'])]

    def process_item(self, spider, item):
        triples = [triple for triple in self.transform_to_triples(item) if triple.object]
        self.sc.insert(triples)
        return item
