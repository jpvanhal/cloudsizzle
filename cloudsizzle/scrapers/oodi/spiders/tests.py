# coding=utf8
import os
import unittest
import datetime

from cloudsizzle.scrapers.oodi.items import CompletedCourseItem, ModuleItem
from cloudsizzle.scrapers.oodi.spiders.oodi import SPIDER
from cloudsizzle.scrapers.mock import MockResponseFactory

RESPONSE_FACTORY = MockResponseFactory(os.path.dirname(__file__))


class ParseCompletedStudies(unittest.TestCase):
    def test_empty_completed_studies(self):
        response = RESPONSE_FACTORY.create_response('',
            'empty_completed_studies.html')
        items = list(SPIDER.parse_completed_studies(response))
        self.assertEqual(0, len(items))

    def test_single_ungrouped_course_in_completed_studies(self):
        response = RESPONSE_FACTORY.create_response('',
            'single_ungrouped_course_in_completed_studies.html')
        items = list(SPIDER.parse_completed_studies(response))
        self.assertTrue(isinstance(items[0], CompletedCourseItem))
        self.assertEqual(1, len(items))
        self.assertEqual('T-79.3001', items[0]['code'])
        self.assertEqual('Logic in computer science: foundations',
            items[0]['name'])
        self.assertEqual('4', items[0]['cr'])
        self.assertEqual('', items[0]['ocr'])
        self.assertEqual('5', items[0]['grade'])
        self.assertEqual(datetime.date(2009, 5, 7), items[0]['date'])
        self.assertEqual('Tomi Janhunen', items[0]['teacher'])

    def test_many_ungrouped_courses_in_completed_studies(self):
        response = RESPONSE_FACTORY.create_response('',
            'many_ungrouped_courses_in_completed_studies.html')
        items = list(SPIDER.parse_completed_studies(response))
        self.assertEqual(3, len(items))
        self.assertEqual('TU-22.1103', items[0]['code'])
        self.assertEqual('T-79.3001', items[1]['code'])
        self.assertEqual('T-121.2100', items[2]['code'])

    def test_one_module_in_completed_studies(self):
        response = RESPONSE_FACTORY.create_response('',
            'one_module_in_completed_studies.html')
        items = list(SPIDER.parse_completed_studies(response))
        self.assertEqual(5, len(items))
        self.assertTrue(isinstance(items[0], ModuleItem))
        self.assertEqual('T220-2', items[0]['code'])
        self.assertEqual('Intermediate Module in Software Technology',
            items[0]['name'])

        self.assertTrue(isinstance(items[1], CompletedCourseItem))
        self.assertEqual('T-106.4155', items[1]['code'])
        self.assertEqual('Operating Systems', items[1]['name'])
        self.assertEqual('5', items[1]['cr'])
        self.assertEqual('', items[1]['ocr'])
        self.assertEqual('3', items[1]['grade'])
        self.assertEqual(datetime.date(2008, 12, 22), items[1]['date'])
        self.assertEqual('Vesa Hirvisalo', items[1]['teacher'])

        self.assertTrue(isinstance(items[4], CompletedCourseItem))
        self.assertEqual('T-106.4200', items[4]['code'])


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ParseCompletedStudies, 'test'))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
