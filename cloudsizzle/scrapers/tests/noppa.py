# coding=utf8
import unittest

from cloudsizzle.scrapers.items import CourseItem, FacultyItem
from cloudsizzle.scrapers.spiders.noppa import SPIDER
from cloudsizzle.scrapers.tests.mock import MockResponse

class NoppaSpiderTestCase(unittest.TestCase):
    def test_parse_faculties(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit',
            'faculty_list.html'
        )
        faculties = list(SPIDER.parse_faculty_list(response))

        self.assertEqual(10, len(faculties))
        self.assertEqual(u'Other separate courses', faculties[0]['name'])
        self.assertEqual(u'Faculty of Chemistry and Materials Sciences',
            faculties[8]['name'])

    def test_parse_departments(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit/il',
            'department_list.html'
        )
        faculty = FacultyItem()
        faculty['name'] = 'Faculty of Information and Natural Sciences'
        departments = list(SPIDER.parse_department_list(response, faculty))

        self.assertEqual(20, len(departments))
        self.assertEqual(u'IL-0', departments[0]['code'])
        self.assertEqual(u'Common courses for the faculty', departments[0]['name'])
        self.assertEqual(u'T3090', departments[18]['code'])
        self.assertEqual(u'Language Centre', departments[18]['name'])

    def test_parse_course_list(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit/il/t3050',
            'course_list.html'
        )
        courses = list(SPIDER.parse_course_list(response))

        self.assertEqual(182, len(courses), 'incorrect amount of courses')
        self.assertEqual(u'T-0.7050', courses[0]['code'], 'wrong course code')
        self.assertEqual(u'T-93.6400', courses[-1]['code'], 'wrong course code')
        self.assertEqual(
            u'Introduction to Postgraduate Studies in Computer Science P',
            courses[0]['name'], 'wrong course name')
        self.assertEqual(u'Yksilölliset opinnot L',
            courses[-1]['name'], 'wrong course name')

    def test_parse_course_overview(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssi/t-76.4115/esite',
            'course_overview.html'
        )
        course = SPIDER.parse_course_overview(response)

        self.assertEqual(u'T-76.4115', course['code'], 'wrong course code')

        self.assertEqual(u'5-8', course['credits'], 'wrong credits')
        self.assertEqual(u'I-III', course['teaching_period'],
            'wrong teaching period')

        expected = u"You learn to apply in a practical software project " \
                   u"computer science\nand software engineering methods and " \
                   u"tools that have been taught on\nother courses. You " \
                   u"learn to evaluate the practical utility of the\n"\
                   u"different methods and tools in various situations. You " \
                   u"learn to\nwork as a software developer in a large group."
        self.assertEqual(expected, course['learning_outcomes'],
            'wrong learning outcomes')

        expected = u"""Studying software engineering tools and practices in the context of <br> a software development project done as a team for a real customer. <br> The project includes project planning, requirements specification, <br> technical design, coding, quality assurance, system delivery and <br> producing documentation related to the previous activities. Course <br> participants generally work in activities related to the technical <br> implementation of the system."""
        self.assertEqual(expected, course['content'], 'wrong content')
        expected =  u"""<a href="https://noppa.tkk.fi/noppa/kurssi/t-76.3601">T-76.3601</a>  (mandatory),   <a href="https://noppa.tkk.fi/noppa/kurssi/t-76.4602">T-76.4602</a>  (recommended), moderate <br> programming skills"""
        self.assertEqual(expected, course['prerequisites'],
            'wrong prerequisites')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NoppaSpiderTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
