# coding=utf8
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.url import urljoin_rfc
from cloudsizzle.scrapers.items import *

class NoppaSpider(BaseSpider):
    domain_name = 'noppa.tkk.fi'
    start_urls = ['https://noppa.tkk.fi/noppa/kurssit']

    def parse_faculty_list(self, response):
        """Parses list of faculties page in Noppa.

        For each faculty in the page, yields a FacultyItem and a Request to
        faculty's list of departments page in Noppa.

        """
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//tr[starts-with(@id, "informal_")]')
        for row in rows:
            loader = ItemLoader(FacultyItem(), selector=row)
            loader.add_xpath('name', 'td/a/text()')
            faculty = loader.load_item()
            department_url = row.select('td/a/@href').extract()[0]
            yield faculty
            yield Request(
                urljoin_rfc(response.url, department_url),
                lambda r: self.parse_department_list(r, faculty)
            )

    def parse_department_list(self, response, faculty):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//tr[starts-with(@id, "informal_")]')
        for row in rows:
            loader = ItemLoader(DepartmentItem(), selector=row)
            loader.item['faculty'] = faculty
            loader.add_xpath('code', 'td[1]/text()')
            loader.add_xpath('name', 'td[2]/a/text()')
            department = loader.load_item()
            url = row.select('td[2]/a/@href').extract()[0]
            yield department
            yield Request(
                urljoin_rfc(response.url, url), 
                lambda r: self.parse_course_list(r, department)
            )

    def parse_course_frontpage(self, response, course):
        overview_url = response.url.replace('/etusivu', '/esite')
        yield Request(
            overview_url, 
            callback=lambda r: parse_course_overview(r, course)
        )

    def parse_course_overview(self, response, course):
        """Parses a course overview page and returns a CourseItem containing 
        the parsed data.
         
        """
        hxs = HtmlXPathSelector(response)
        loader = ItemLoader(CourseOverviewItem(),
            selector=hxs.select('//table[contains(@class, "courseBrochure")]'))

        def build_xpath(*args):
            condition = ' or '.join(
                'contains(text(), "{0}")'.format(header) for header in args)
            xpath = 'tr/td[{0}]/following-sibling::td'.format(condition)
            return xpath
        
        loader.item['course'] = course
        loader.add_xpath(
            'credits', 
            build_xpath(
                'Credits', 
                'Laajuus', 
                'Omfattning'
            ), 
            re=r'(\d+(?:-\d+)?)'
        )
        loader.add_xpath(
            'teaching_period', 
            build_xpath(
                'Teaching period', 
                'Opetusjakso', 
                'Undervisningsperiod'
            )
        )
        loader.add_xpath(
            'learning_outcomes', 
            build_xpath(
                'Learning outcomes', 
                'Osaamistavoitteet', 
                'Kompetensmålsättningar'
            )
        )
        loader.add_xpath(
            'content', 
            build_xpath(
                'Content', 
                'Sisältö', 
                'Innehåll'
            )
        )
        loader.add_xpath(
            'prerequisites', 
            build_xpath(
                'Prerequisites', 
                'Esitiedot', 
                'Förkunskaper'
            )
        )
        return loader.load_item()

    def parse_course_list(self, response, department):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//tr[starts-with(@id, "informal_")]')
        for row in rows:
            loader = ItemLoader(CourseItem(), selector=row)
            loader.item['department'] = department
            loader.add_xpath('code', 'td[1]/text()')
            loader.add_xpath('name', 'td[2]/a/text()')
            course = loader.load_item()
            course_url = row.select('td[2]/a/@href').extract()[0]
            yield course
            yield Request(
               urljoin_rfc(response.url, course_url), 
                lambda r: self.parse_course_frontpage(r, course)
            )
        

    parse = parse_faculty_list

SPIDER = NoppaSpider()
