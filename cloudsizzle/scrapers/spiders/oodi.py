import urllib
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from cloudsizzle.scrapers.spiders.weblogin import WebloginSpider
from cloudsizzle.scrapers.items import CompletedCourseItem, ItemLoader

class OodiSpider(WebloginSpider):
    domain_name = 'oodi.tkk.fi'
    start_urls = ['https://oodi.tkk.fi/w/oodishibboleth.jsp']

    def parse(self, response):
        params = urllib.url_encode({
            'Kieli': 6,
            'MD5avain': self._session_hash,
            'NaytSuor': 1,
            'exvalittu': 1
        })
        completed_studies_url = 'https://oodi.tkk.fi/w/omatopinn.jsp?{0}'.format(params)
        yield Request(completed_studies_url, callback=self.completed_studies)

    def parse_completed_studies(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//tr[td[starts-with(@class, "tyyli")]]')
        for row in rows:
            loader = ItemLoader(CompletedCourseItem(), selector=row)
            loader.add_xpath('code', 'td[1]/a/text()')
            loader.add_xpath('name', 'td[2]/text()')
            loader.add_xpath('cr', 'td[3]/text()')
            loader.add_xpath('ocr', 'td[4]/text()')
            loader.add_xpath('grade', 'td[5]/text()')
            loader.add_xpath('date', 'td[6]/text()')
            loader.add_xpath('teacher', 'td[7]/text()')
            yield loader.load_item()
        #hxs.select('//tr[td[starts-with(@class, "taso2")]]')

SPIDER = OodiSpider()
