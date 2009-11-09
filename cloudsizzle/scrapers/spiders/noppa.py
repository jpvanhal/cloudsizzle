from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose, Join
from scrapy.selector import HtmlXPathSelector
from cloudsizzle.scrapers.items import CourseItem

class CourseItemLoader(XPathItemLoader):
    default_item_class = CourseItem
    default_output_processor = Compose(Join(), unicode.strip)

class NoppaSpider(CrawlSpider):
    domain_name = 'noppa.tkk.fi'
    start_urls = ['https://noppa.tkk.fi/noppa/kurssit']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/noppa/kurssit/[a-z]+$', ))),
        Rule(SgmlLinkExtractor(allow=(r'/noppa/kurssit/[a-z]+/[a-z0-9-]+$', )),
             callback='parse_course_list'),
        Rule(SgmlLinkExtractor(allow=(r'/noppa/kurssi/[a-z0-9-\.]+/esite', )),
             callback='parse_course_overview'),
    )

    def parse_course_overview(self, response):
        hxs = HtmlXPathSelector(response)
        loader = CourseItemLoader(
            selector=hxs.select('//table[contains(@class, "courseBrochure")]'))

        def build_xpath(*args):
            condition = ' or '.join(
                'contains(text(), "{0}")'.format(header) for header in args)
            xpath = 'tr/td[{0}]/following-sibling::td/node()'.format(condition)
            return xpath

        loader.add_value('code', self.parse_course_code_from_course_page(response))
        loader.add_xpath('credits', build_xpath('Credits'), re=r'(\d+(?:-\d+)?)')
        loader.add_xpath('teaching_period', build_xpath('Teaching period'))
        loader.add_xpath('learning_outcomes', build_xpath('Learning outcomes'))
        loader.add_xpath('content', build_xpath('Content'))
        loader.add_xpath('prerequisites', build_xpath('Prerequisites'))
        return loader.load_item()

    def parse_course_code_from_course_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//title/text()').extract()[0]
        course_code = title.split(' ')[0]
        return course_code

    def parse_course_list(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//table[@id="courseTableView"]/tr')

        # ignore header row and last empty row
        for row in rows[1:-1]:
            course = CourseItem()
            course['code'] = row.select('td[1]/text()')[0].extract().strip()
            course['name'] = row.select('td[2]/a/text()')[0].extract().strip()
            yield course

SPIDER = NoppaSpider()
