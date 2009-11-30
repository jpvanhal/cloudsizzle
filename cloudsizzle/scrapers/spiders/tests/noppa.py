# coding=utf8
import unittest

from scrapy.http import Request
from cloudsizzle.scrapers.items import CourseItem, FacultyItem, DepartmentItem, CourseOverviewItem
from cloudsizzle.scrapers.spiders.noppa import SPIDER
from cloudsizzle.scrapers.spiders.tests.mock import MockResponse

class ParseFaculties(unittest.TestCase):
    def setUp(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit',
            'faculty_list.html'
        )
        items = list(SPIDER.parse_faculty_list(response))
        self.faculties = [item for item in items if isinstance(item, FacultyItem)]
        self.requests = [item for item in items if isinstance(item, Request)]

    def test_correct_number_of_faculties_scraped(self):
        self.assertEqual(5, len(self.faculties))

    def test_faculty_ids_scraped(self):
        self.assertEqual(u'eri', self.faculties[0]['id'])
        self.assertEqual(u'km', self.faculties[-1]['id'])

    def test_faculty_names_scraped(self):
        self.assertEqual(u'Other separate courses', self.faculties[0]['name'])
        self.assertEqual(u'Faculty of Chemistry and Materials Sciences',
            self.faculties[-1]['name'])

    def test_requests_to_department_list_pages_generated(self):
        self.assertTrue(isinstance(self.requests[0], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssit/eri',
            self.requests[0].url)
        self.assertEqual(id(self.faculties[0]), id(self.requests[0].meta['faculty']))

        self.assertTrue(isinstance(self.requests[-1], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssit/km',
            self.requests[-1].url)
        self.assertEqual(id(self.faculties[-1]), id(self.requests[-1].meta['faculty']))

class ParseDepartments(unittest.TestCase):
    def setUp(self):
        self.faculty = FacultyItem()
        self.faculty['name'] = 'Faculty of Information and Natural Sciences'

        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit/il',
            'department_list.html')
        response.request.meta['faculty'] = self.faculty

        items = list(SPIDER.parse_department_list(response))
        self.departments = [item for item in items if isinstance(item, DepartmentItem)]
        self.requests = [item for item in items if isinstance(item, Request)]

    def test_correct_number_of_departments_scraped(self):
        self.assertEqual(10, len(self.departments))

    def test_department_names_scraped(self):
        self.assertEqual(u'Common courses for the faculty', self.departments[0]['name'])
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
        self.assertEqual(id(self.departments[0]), id(self.requests[0].meta['department']))
        self.assertTrue(isinstance(self.requests[-1], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssit/il/t3090',
            self.requests[-1].url)
        self.assertEqual(id(self.departments[-1]), id(self.requests[-1].meta['department']))

class ParseCourses(unittest.TestCase):
    def setUp(self):
        self.department = DepartmentItem()
        self.department['name'] = u'Department of Computer Science and Engineering'

        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssit/il/t3050',
            'course_list.html')
        response.request.meta['department'] = self.department

        items = list(SPIDER.parse_course_list(response))
        self.courses = [item for item in items if isinstance(item, CourseItem)]
        self.requests = [item for item in items if isinstance(item, Request)]

    def test_correct_number_of_courses_scraped(self):
        self.assertEqual(182, len(self.courses))

    def test_course_codes_scraped(self):
        self.assertEqual(u'T-0.7050', self.courses[0]['code'])
        self.assertEqual(u'T-93.6400', self.courses[-1]['code'])

    def test_course_names_scraped(self):
        self.assertEqual(
            u'Introduction to Postgraduate Studies in Computer Science P',
            self.courses[0]['name'])
        self.assertEqual(u'Yksilölliset opinnot L', self.courses[-1]['name'])

    def test_courses_have_department_set(self):
        self.assertEqual(id(self.department), id(self.courses[0]['department']))

    def test_requests_to_course_front_page_generated(self):
        self.assertTrue(isinstance(self.requests[0], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssi/t-0.7050/etusivu',
            self.requests[0].url)
        self.assertEqual(id(self.courses[0]), id(self.requests[0].meta['course']))
        self.assertTrue(isinstance(self.requests[-1], Request))
        self.assertEqual('https://noppa.tkk.fi/noppa/kurssi/t-93.6400/etusivu',
            self.requests[-1].url)
        self.assertEqual(id(self.courses[-1]), id(self.requests[-1].meta['course']))

class ParseCourseOverview(unittest.TestCase):
    def setUp(self):
        self.course = CourseItem()
        self.course['code'] = 'T-76.4115'
        self.course['name'] = 'Software Development Project I'

        response = MockResponse(
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
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParseFaculties, 'test'))
    suite.addTest(unittest.makeSuite(ParseDepartments, 'test'))
    suite.addTest(unittest.makeSuite(ParseCourses, 'test'))
    suite.addTest(unittest.makeSuite(ParseCourseOverview, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
