# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from .items import FacultyItem, DepartmentItem, CourseItem, CourseOverviewItem
from cloudsizzle.kp import SIBConnection, Triple, literal, uri, bnode

class SIBPipeline(object):
    def __init__(self):
        self.sc = SIBConnection(method='preconfigured')
        self.sc.open()

    def __del__(self):
        self.sc.close()

    def transform_to_triples(self, item):
        if isinstance(item, FacultyItem):
            return [
                Triple(item['code'], 'rdf:type', 'Faculty'),
                Triple(item['code'], 'name', item['name'])]
        elif isinstance(item, DepartmentItem):
            return [
                Triple(item['code'], 'rdf:type', 'Department'),
                Triple(item['code'], 'name', item['name']),
                Triple(item['code'], 'faculty', uri(item['faculty']['code']))]
        elif isinstance(item, CourseItem):
            return [
                Triple(item['code'], 'rdf:type', 'Course'),
                Triple(item['code'], 'name', item['name']),
                Triple(item['code'], 'department', uri(item['department']['code']))]
        elif isinstance(item, CourseOverviewItem):
            subject = item['course']['code']
            return [
                Triple(subject, 'extent', item['extent']),
                Triple(subject, 'teaching_period', item['teaching_period']),
                Triple(subject, 'learning_outcomes', item['learning_outcomes']),
                Triple(subject, 'content', item['content']),
                Triple(subject, 'prerequisites', item['prerequisites']),
                Triple(subject, 'study_materials', item['study_materials'])]

    def process_item(self, spider, item):
        triples = [triple for triple in self.transform_to_triples(item) if triple.object]
        self.sc.insert(triples)
        return item
