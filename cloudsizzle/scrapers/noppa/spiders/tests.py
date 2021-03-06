# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2010 CloudSizzle Team
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import os
import unittest

from scrapy.http import Request
from cloudsizzle.scrapers.noppa.items import CourseItem, FacultyItem, \
    DepartmentItem
from cloudsizzle.scrapers.mock import MockResponseFactory
from cloudsizzle.scrapers.noppa.spiders.noppa import SPIDER

RESPONSE_FACTORY = MockResponseFactory(os.path.dirname(__file__))


class ParseFaculties(unittest.TestCase):

    def setUp(self):
        response = RESPONSE_FACTORY.create_response(
            'https://noppa.tkk.fi/noppa/kurssit',
            'faculty_list.html')
        items = list(SPIDER.parse_faculty_list(response))
        self.faculties = [item for item in items
                          if isinstance(item, FacultyItem)]
        self.requests = [item for item in items if isinstance(item, Request)]

    def test_correct_number_of_faculties_scraped(self):
        self.assertEqual(5, len(self.faculties))

    def test_faculty_codes_scraped(self):
        self.assertEqual(u'eri', self.faculties[0]['code'])
        self.assertEqual(u'km', self.faculties[-1]['code'])

    def test_faculty_names_scraped(self):
        self.assertEqual(u'Other separate courses', self.faculties[0]['name'])
        self.assertEqual(u'Faculty of Chemistry and Materials Sciences',
            self.faculties[-1]['name'])

    def test_requests_to_department_list_pages_generated(self):
        self.assertTrue(isinstance(self.requests[0], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssit/eri',
            self.requests[0].url)
        self.assertTrue(self.faculties[0] is self.requests[0].meta['faculty'])

        self.assertTrue(isinstance(self.requests[-1], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssit/km',
            self.requests[-1].url)
        self.assertTrue(self.faculties[-1] is self.requests[-1].meta['faculty'])


class ParseDepartments(unittest.TestCase):

    def setUp(self):
        self.faculty = FacultyItem()
        self.faculty['name'] = 'Faculty of Information and Natural Sciences'

        response = RESPONSE_FACTORY.create_response(
            'https://noppa.tkk.fi/noppa/kurssit/il',
            'department_list.html')
        response.request.meta['faculty'] = self.faculty

        items = list(SPIDER.parse_department_list(response))
        self.departments = [item for item in items
                            if isinstance(item, DepartmentItem)]
        self.requests = [item for item in items if isinstance(item, Request)]

    def test_correct_number_of_departments_scraped(self):
        self.assertEqual(10, len(self.departments))

    def test_department_names_scraped(self):
        self.assertEqual(u'Common courses for the faculty',
             self.departments[0]['name'])
        self.assertEqual(u'Language Centre', self.departments[-1]['name'])

    def test_department_codes_scraped(self):
        self.assertEqual(u'IL-0', self.departments[0]['code'])
        self.assertEqual(u'T3090', self.departments[-1]['code'])

    def test_departments_have_faculty_set(self):
        self.assertEqual(id(self.faculty), id(self.departments[0]['faculty']))

    def test_requests_to_course_list_pages_generated(self):
        self.assertTrue(isinstance(self.requests[0], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssit/il/il-0',
            self.requests[0].url)
        self.assertTrue(
            self.departments[0] is self.requests[0].meta['department'])
        self.assertTrue(isinstance(self.requests[-1], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssit/il/t3090',
            self.requests[-1].url)
        self.assertTrue(
            self.departments[-1] is self.requests[-1].meta['department'])


class ParseCourses(unittest.TestCase):

    def setUp(self):
        self.department = DepartmentItem()
        self.department['name'] = \
            u'Department of Computer Science and Engineering'

        response = RESPONSE_FACTORY.create_response(
            'https://noppa.tkk.fi/noppa/kurssit/il/t3050',
            'course_list.html')
        response.request.meta['department'] = self.department

        items = list(SPIDER.parse_course_list(response))
        self.courses = [item for item in items if isinstance(item, CourseItem)]
        self.requests = [item for item in items if isinstance(item, Request)]

    def test_correct_number_of_courses_scraped(self):
        self.assertEqual(22, len(self.courses))

    def test_course_codes_scraped(self):
        self.assertEqual(u'T-0.7050', self.courses[0]['code'])
        self.assertEqual(u'T-106.3101', self.courses[-1]['code'])

    def test_course_names_scraped(self):
        self.assertEqual(
            u'Introduction to Postgraduate Studies in Computer Science P',
            self.courses[0]['name'])
        self.assertEqual(u'Ohjelmoinnin jatkokurssi T2 (C-kieli)',
            self.courses[-1]['name'])

    def test_courses_have_department_set(self):
        self.assertTrue(self.department is self.courses[0]['department'])

    def test_crawls_to_next_course_list_page(self):
        request = self.requests[0]
        self.assertTrue('linkFwd' in request.url)
        self.assertTrue(request.meta['department'] is self.department)


class ParseCourseOverview(unittest.TestCase):

    def setUp(self):
        self.course = CourseItem()
        self.course['code'] = 'T-76.4115'
        self.course['name'] = 'Software Development Project I'

        response = RESPONSE_FACTORY.create_response(
            'https://noppa.tkk.fi/noppa/kurssi/t-76.4115/esite',
            'course_overview.html')
        response.request.meta['course'] = self.course

        self.overview = SPIDER.parse_course_overview(response)

    def test_course_extent_scraped(self):
        self.assertEqual(u'5-8', self.overview['extent'])

    def test_teaching_period_scraped(self):
        self.assertEqual(u'I-III', self.overview['teaching_period'])

    def test_learning_outcomes_scraped(self):
        expected = (
            u"You learn to apply in a practical software project computer "
            u"science and software engineering methods and tools that have "
            u"been taught on other courses. You learn to evaluate the "
            u"practical utility of the different methods and tools in various "
            u"situations. You learn to work as a software developer in a large"
            u" group.")
        self.assertEqual(expected, self.overview['learning_outcomes'])

    def test_course_content_scraped(self):
        expected = (
            u"Studying software engineering tools and practices in the context"
            u" of a software development project done as a team for a real "
            u"customer. The project includes project planning, requirements "
            u"specification, technical design, coding, quality assurance, "
            u"system delivery and producing documentation related to the "
            u"previous activities. Course participants generally work in "
            u"activities related to the technical implementation of the "
            u"system.")
        self.assertEqual(expected, self.overview['content'])

    def test_prerequisites_scraped(self):
        expected = (
            u"T-76.3601 (mandatory), T-76.4602 (recommended), moderate "
            u"programming skills")
        self.assertEqual(expected, self.overview['prerequisites'])

    def test_study_materials_scraped(self):
        self.assertEqual(u"Instructions for the project work.",
            self.overview['study_materials'])

    def test_overview_has_course_reference_set(self):
        self.assertEqual(id(self.course), id(self.overview['course']))


def suite():
    tests_suite = unittest.TestSuite()
    tests_suite.addTest(unittest.makeSuite(ParseFaculties, 'test'))
    tests_suite.addTest(unittest.makeSuite(ParseDepartments, 'test'))
    tests_suite.addTest(unittest.makeSuite(ParseCourses, 'test'))
    tests_suite.addTest(unittest.makeSuite(ParseCourseOverview, 'test'))
    return tests_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
