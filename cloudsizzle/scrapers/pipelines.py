# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from cloudsizzle.scrapers.items import FacultyItem, DepartmentItem, CourseItem, CourseOverviewItem, CompletedCourseItem, ModuleItem
from kpwrapper import SIBConnection, Triple, literal, uri, bnode
from scrapy.conf import settings

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

    @property
    def asi_username(self):
        if not hasattr(self, '_asi_username'):
            self._asi_username = settings['ASI_USERNAME']
            if not self._asi_username:
                self._asi_username = raw_input('ASI Username: ')
        return self._asi_username

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
        elif isinstance(item, CompletedCourseItem):
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
