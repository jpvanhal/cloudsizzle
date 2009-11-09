# coding=utf8
import os
from cloudsizzle.scrapers.spiders.noppa import SPIDER
from scrapy.http import HtmlResponse

def MockResponse(url, filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    return HtmlResponse(url=url, body=open(filename).read())

class TestParseCourseList:
    def __init__(self):
        response = MockResponse('https://noppa.tkk.fi/noppa/kurssit/il/t3050',
            'course_list.html')
        self.courses = list(SPIDER.parse_course_list(response))

    def test_parse_course_list_finds_all_courses(self):
        assert len(self.courses) == 182

    def test_parse_course_list_scrapes_course_code(self):
        assert self.courses[0]['code'] == u'T-0.7050'
        assert self.courses[-1]['code'] == u'T-93.6400'

    def test_parse_course_list_scrapes_course_name(self):
        assert self.courses[0]['name'] == u'Introduction to Postgraduate Studies in Computer Science P'
        assert self.courses[-1]['name'] == u'Yksilölliset opinnot L'

class TestParseCourseOverview:
    def __init__(self):
        response = MockResponse(
            'https://noppa.tkk.fi/noppa/kurssi/t-76.4115/esite',
            'course_overview.html')
        self.course = SPIDER.parse_course_overview(response)

    def test_parse_course_overview_scrapes_course_code(self):
        assert self.course['code'] == u'T-76.4115'

    def test_parse_course_overview_scrapes_credits(self):
        assert self.course['credits'] == u'5-8'

    def test_parse_course_overview_scrapes_teaching_period(self):
        assert self.course['teaching_period'] == u'I-III'

    def test_parse_course_overview_scrapes_learning_outcomes(self):
        expected = u"You learn to apply in a practical software project " \
                   u"computer science\nand software engineering methods and " \
                   u"tools that have been taught on\nother courses. You " \
                   u"learn to evaluate the practical utility of the\n"\
                   u"different methods and tools in various situations. You " \
                   u"learn to\nwork as a software developer in a large group."
        assert self.course['learning_outcomes'] == expected

    def test_parse_course_overview_scrapes_content(self):
        expected = u"""Studying software engineering tools and practices in the context of <br> a software development project done as a team for a real customer. <br> The project includes project planning, requirements specification, <br> technical design, coding, quality assurance, system delivery and <br> producing documentation related to the previous activities. Course <br> participants generally work in activities related to the technical <br> implementation of the system."""
        assert self.course['content'] == expected

    def test_parse_course_overview_scrapes_prerequisites(self):
        expected =  u"""<a href="https://noppa.tkk.fi/noppa/kurssi/t-76.3601">T-76.3601</a>  (mandatory),   <a href="https://noppa.tkk.fi/noppa/kurssi/t-76.4602">T-76.4602</a>  (recommended), moderate <br> programming skills"""
        assert self.course['prerequisites'] == expected
