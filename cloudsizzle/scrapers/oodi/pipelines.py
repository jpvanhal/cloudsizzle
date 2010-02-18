# coding=utf-8
"""
Pipeline for storing scraped triples to SIB.

See: http://doc.scrapy.org/topics/item-pipeline.html

"""
from cloudsizzle.scrapers.oodi.items import CompletedCourseItem, ModuleItem
from cloudsizzle.kp import SIBConnection, Triple, uri
from scrapy.conf import settings
from scrapy.core.exceptions import DropItem

CLOUDSIZZLE_RDF_NAMESPACE = 'http://cloudsizzle.cs.hut.fi/ontology/'
ASI_PEOPLE_RDF_NAMESPACE = 'http://cos.alpha.sizl.org/people'


class SIBPipeline(object):

    def __init__(self):
        self.asi_user_id = settings['ASI_USER_ID']
        if not self.asi_user_id:
            self.asi_user_id = raw_input('ASI User ID: ')

        self.sc = SIBConnection(method='preconfigured')
        self.sc.open()

    def __del__(self):
        if hasattr(self, 'sc'):
            self.sc.close()

    def transform_to_triples(self, item):
        if isinstance(item, CompletedCourseItem):
            subject = '{0}people/{1}/courses/completed/{2}'.format(
                CLOUDSIZZLE_RDF_NAMESPACE, self.asi_user_id, item['code'])
            user = '{0}/ID#{1}'.format(
                ASI_PEOPLE_RDF_NAMESPACE, self.asi_user_id)
            return [
                Triple(subject, 'rdf:type', 'CompletedCourse'),
                Triple(subject, 'user', uri(user)),
                Triple(subject, 'code', item['code']),
                Triple(subject, 'name', item['name']),
                Triple(subject, 'cr', item['cr']),
                Triple(subject, 'ocr', item['ocr']),
                Triple(subject, 'grade', item['grade']),
                Triple(subject, 'date', item['date'].isoformat()),
                Triple(subject, 'teacher', item['teacher'])]
        elif isinstance(item, ModuleItem):
            raise DropItem("Modules are not needed in SIB: %s" % item)

    def process_item(self, spider, item):
        triples = [triple for triple in self.transform_to_triples(item)
                   if triple.object]
        self.sc.insert(triples)
        return item
