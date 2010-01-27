# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from cloudsizzle.scrapers.items import FacultyItem, DepartmentItem, CourseItem, CourseOverviewItem, CompletedCourseItem, ModuleItem
from cloudsizzle.kp import SIBConnection, Triple, literal, uri, bnode
from scrapy.conf import settings

class SIBPipeline(object):
    def __init__(self):
        self.asi_username = settings['ASI_USERNAME']
        if not self.asi_username:
            self.asi_username = raw_input('ASI Username: ')

        self.sc = SIBConnection(method='preconfigured')
        self.sc.open()

    def __del__(self):
        self.sc.close()

    def transform_to_triples(self, item):
        if isinstance(item, CompletedCourseItem):
            return [
                Triple(self.asi_username, 'rdf:type', 'Person'),
                Triple(self.asi_username, 'has_completed', bnode('id')),
                Triple(bnode('id'), 'rdf:type', 'CompletedCourse'),
                Triple(bnode('id'), 'code', item['code']),
                Triple(bnode('id'), 'name', item['name']),
                Triple(bnode('id'), 'cr', item['cr']),
                Triple(bnode('id'), 'ocr', item['ocr']),
                Triple(bnode('id'), 'grade', item['grade']),
                Triple(bnode('id'), 'date', item['date'].isoformat()),
                Triple(bnode('id'), 'teacher', item['teacher'])]
                # TODO: module is missing
        elif isinstance(item,ModuleItem):
            return [
                Triple(item['code'], 'rdf:type', 'Module'),
                Triple(item['code'], 'name', item['name'])]

    def process_item(self, spider, item):
        triples = [triple for triple in self.transform_to_triples(item) if triple.object]
        self.sc.insert(triples)
        return item
