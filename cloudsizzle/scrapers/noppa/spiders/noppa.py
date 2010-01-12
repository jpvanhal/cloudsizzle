# coding=utf8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.url import urljoin_rfc
from cloudsizzle.scrapers.noppa.items import FacultyItem, DepartmentItem, CourseItem, CourseOverviewItem
from cloudsizzle.scrapers.items import ItemLoader

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
            department_url = row.select('td/a/@href').extract()[0]
            loader.add_value('code', department_url.split('/')[-1])
            faculty = loader.load_item()
            yield faculty
            yield Request(
                urljoin_rfc(response.url, department_url),
                meta={'faculty': faculty}, callback=self.parse_department_list
            )

    def parse_department_list(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//tr[starts-with(@id, "informal_")]')
        for row in rows:
            loader = ItemLoader(DepartmentItem(), selector=row)
            loader.item['faculty'] = response.request.meta['faculty']
            loader.add_xpath('code', 'td[1]/text()')
            loader.add_xpath('name', 'td[2]/a/text()')
            department = loader.load_item()
            url = row.select('td[2]/a/@href').extract()[0]
            yield department
            yield Request(
                urljoin_rfc(response.url, url),
                meta={'department': department}, callback=self.parse_course_list
            )

    def parse_course_overview(self, response):
        """Parses a course overview page and returns a CourseItem containing
        the parsed data.

        """
        hxs = HtmlXPathSelector(response)
        xpath = '//table[contains(@class, "courseBrochure")]'
        loader = ItemLoader(CourseOverviewItem(), selector=hxs.select(xpath))
        loader.item['course'] = response.request.meta['course']
        loader.add_xpath('extent', 'tr[1]/td[2]', re=r'(\d+(?:-\d+)?)')
        loader.add_xpath('teaching_period', 'tr[2]/td[2]')
        loader.add_xpath('learning_outcomes', 'tr[3]/td[2]')
        loader.add_xpath('content', 'tr[4]/td[2]')
        loader.add_xpath('prerequisites', 'tr[5]/td[2]')
        loader.add_xpath('study_materials', 'tr[11]/td[2]')
        return loader.load_item()

    def parse_course_list(self, response):
        hxs = HtmlXPathSelector(response)
        department = response.request.meta['department']

        # Crawl to the next course list page
        try:
            next_page = hxs.select('//a[@id="linkFwd"]/@href').extract()[0]
        except IndexError:
            # This is the last page in pagination
            pass
        else:
            yield Request(
                url="https://noppa.tkk.fi" + next_page,
                meta={'department': department},
                callback=self.parse_course_list)

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
                urljoin_rfc(response.url, course_url[:-7] + 'esite'),
                meta={'course': course}, callback=self.parse_course_overview
            )


    parse = parse_faculty_list

SPIDER = NoppaSpider()
