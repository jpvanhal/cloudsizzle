# coding=utf8
import unittest

from cloudsizzle.scrapers.items import CourseItem, FacultyItem, DepartmentItem, CourseOverviewItem
from cloudsizzle.scrapers.spiders.noppa import SPIDER
from cloudsizzle.scrapers.tests.mock import MockResponse

class NoppaSpiderTestCase(unittest.TestCase):
    def test_parse_faculties(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit',
            'faculty_list.html'
        )
        returned = list(SPIDER.parse_faculty_list(response))
        faculties = returned[::2]
        requests = returned[1::2]

        self.assertEqual(5, len(faculties))
        self.assertEqual(u'Other separate courses', faculties[0]['name'])
        self.assertEqual(u'Faculty of Chemistry and Materials Sciences',
            faculties[4]['name'])

    def test_parse_departments(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit/il',
            'department_list.html'
        )
        faculty = FacultyItem()
        faculty['name'] = 'Faculty of Information and Natural Sciences'
        returned = list(SPIDER.parse_department_list(response, faculty))
        departments = returned[::2]
        requests = returned[1::2]
        
        self.assertEqual(10, len(departments))
        self.assertEqual(u'IL-0', departments[0]['code'])
        self.assertEqual(u'Common courses for the faculty', departments[0]['name'])
        self.assertEqual(u'T3090', departments[9]['code'])
        self.assertEqual(u'Language Centre', departments[9]['name'])

    def test_parse_course_list(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit/il/t3050',
            'course_list.html'
        )
        department = DepartmentItem()
        department['name'] = 'Department of Computer Science and Engineering'
        returned = list(SPIDER.parse_course_list(response, department))
        courses = returned[::2]
        requests = returned[1::2]

        self.assertEqual(182, len(courses))
        self.assertEqual(u'T-0.7050', courses[0]['code'])
        self.assertEqual(u'T-93.6400', courses[-1]['code'])
        self.assertEqual(
            u'Introduction to Postgraduate Studies in Computer Science P',
            courses[0]['name'])
        self.assertEqual(u'Yksilölliset opinnot L', courses[-1]['name'],)

    def test_parse_course_overview(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssi/t-76.4115/esite',
            'course_overview.html'
        )
        course = CourseItem()
        course['code'] = 'T-76.4115'
        course['name'] = 'Software Development Project I'
        overview = SPIDER.parse_course_overview(response, course)

        self.assertEqual(u'5-8', overview['credits'])
        self.assertEqual(u'I-III', overview['teaching_period'])

        expected = u"You learn to apply in a practical software project " \
                   u"computer science and software engineering methods and " \
                   u"tools that have been taught on other courses. You " \
                   u"learn to evaluate the practical utility of the "\
                   u"different methods and tools in various situations. You " \
                   u"learn to work as a software developer in a large group."
        self.assertEqual(expected, overview['learning_outcomes'])
        
        expected = u"""Studying software engineering tools and practices in the context of a software development project done as a team for a real customer. The project includes project planning, requirements specification, technical design, coding, quality assurance, system delivery and producing documentation related to the previous activities. Course participants generally work in activities related to the technical implementation of the system."""
        self.assertEqual(expected, overview['content'])
        expected =  u"""T-76.3601 (mandatory), T-76.4602 (recommended), moderate programming skills"""
        self.assertEqual(expected, overview['prerequisites'])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NoppaSpiderTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
