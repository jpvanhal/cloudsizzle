# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from cloudsizzle.scrapers.items import FacultyItem, DepartmentItem, CourseItem, CourseOverviewItem
from kpwrapper import SIBConnection, Triple, literal

class UTF8Pipeline(object):
    def process_item(self, domain, item):
        for field, value in item.items():
            if isinstance(value, basestring):
                item[field] = value.encode('utf-8')
        return item

class SIBPipeline(object):
    def __init__(self):
        self.sc = SIBConnection('SIB console', 'preconfigured')
        self.sc.open()

    def __del__(self):
        self.sc.close()

    def transform_to_triples(self, item):
        if isinstance(item, FacultyItem):
            yield Triple(item['name'], 'rdf:type', 'Faculty')
        elif isinstance(item, DepartmentItem):
            yield Triple(item['code'], 'rdf:type', 'Department')
            yield Triple(item['code'], 'name', item['name'])
        elif isinstance(item, CourseItem):
            yield Triple(item['code'], 'rdf:type', 'Course')
            yield Triple(item['code'], 'name', item['name'])
        elif isinstance(item, CourseOverviewItem):
            subject = item['course']['code']
            yield Triple(subject, 'extent', item['extent'])
            yield Triple(subject, 'teaching_period', item['teaching_period'])
            yield Triple(subject, 'learning_outcomes', item['learning_outcomes'])
            yield Triple(subject, 'content', item['content'])
            yield Triple(subject, 'prerequisites', item['prerequisites'])
            yield Triple(subject, 'study_materials', item['study_materials'])

    def process_item(self, domain, item):
        triples = [triple for triple in self.transform_to_triples(item)]
        self.sc.insert(triples)
        return item
