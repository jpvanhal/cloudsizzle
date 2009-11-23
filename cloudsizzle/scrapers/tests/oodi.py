# coding=utf8
import unittest

from scrapy.http import Request
from cloudsizzle.scrapers.items import CourseItem, FacultyItem, DepartmentItem, CourseOverviewItem
from cloudsizzle.scrapers.spiders.oodi import SPIDER
from cloudsizzle.scrapers.tests.mock import MockResponse

class ParseCompletedStudies(unittest.TestCase):
    def setUp(self):
        response = MockResponse('', 'completed_studies.html')
        self.items = list(SPIDER.parse_completed_studies(response))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParseCompletedStudies, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
