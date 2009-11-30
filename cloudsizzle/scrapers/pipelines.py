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
            if isinstance(value, unicode):
                item[field] = value.encode('utf-8')
        return item

class SIBPipeline(object):
    def __init__(self):
        self.sc = SIBConnection(method='preconfigured')
        self.sc.open()

    def __del__(self):
        self.sc.close()

    def transform_to_triples(self, item):
        if isinstance(item, FacultyItem):
            return [
                Triple(item['id'], 'rdf:type', 'Faculty'),
                Triple(item['id'], 'name', item['name'])]
        elif isinstance(item, DepartmentItem):
            return [
                Triple(item['code'], 'rdf:type', 'Department'),
                Triple(item['code'], 'name', item['name']),
                Triple(item['code'], 'faculty', item['faculty']['id'])]
        elif isinstance(item, CourseItem):
            return [
                Triple(item['code'], 'rdf:type', 'Course'),
                Triple(item['code'], 'name', item['name']),
                Triple(item['code'], 'department', item['department']['code'])]
        elif isinstance(item, CourseOverviewItem):
            subject = item['course']['code']
            return [
                Triple(subject, 'extent', item['extent']),
                Triple(subject, 'teaching_period', item['teaching_period']),
                Triple(subject, 'learning_outcomes', item['learning_outcomes']),
                Triple(subject, 'content', item['content']),
                Triple(subject, 'prerequisites', item['prerequisites']),
                Triple(subject, 'study_materials', item['study_materials'])]

    def process_item(self, domain, item):
        triples = self.transform_to_triples(item)
        self.sc.insert(triples)
        return item
