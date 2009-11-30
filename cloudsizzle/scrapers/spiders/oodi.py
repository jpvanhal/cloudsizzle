import urllib
import urlparse
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from cloudsizzle.scrapers.spiders.weblogin import WebloginSpider
from cloudsizzle.scrapers.items import CompletedCourseItem, ModuleItem, ItemLoader

class OodiSpider(WebloginSpider):
    domain_name = 'oodi.tkk.fi'
    login_url = 'https://oodi.tkk.fi/w/oodishibboleth.jsp'

    def parse(self, response):
        session_hash = self.parse_session_hash(response)
        params = urllib.urlencode({
            'Kieli': 6,
            'MD5avain': session_hash,
            'NaytSuor': 1,
            'exvalittu': 1
        })
        completed_studies_url = 'https://oodi.tkk.fi/w/omatopinn.jsp?{0}'.format(params)
        yield Request(url=completed_studies_url, callback=self.parse_completed_studies)

    def parse_session_hash(self, response):
        extractor = SgmlLinkExtractor(allow=r'/w/valikko\.jsp', tags='frame', attrs=('src', ))
        link = extractor.extract_links(response)[0]
        query = urlparse.urlparse(link.url).query
        params = urlparse.parse_qs(query)
        return params['MD5avain'][0]

    def parse_completed_studies(self, response):
        hxs = HtmlXPathSelector(response)
        current_module = None
        for row in hxs.select('//table[@class="eisei"]/tbody/tr[td]'):
            is_module = row.select('td/a/img')
            is_ungrouped_course = row.select('td[@class="tyyli0" or @class="tyyli1"]')
            if is_module:
                loader = ItemLoader(ModuleItem(), selector=row)
                loader.add_xpath('code', 'td[1]/a/text()')
                loader.add_xpath('name', 'td[2]/text()')
                current_module = loader.load_item()
                yield current_module
            elif is_ungrouped_course:
                loader = ItemLoader(CompletedCourseItem(), selector=row)
                loader.add_xpath('code', 'td[1]/a/text()')
                loader.add_xpath('name', 'td[2]/text()')
                loader.add_xpath('cr', 'td[3]/text()')
                loader.add_xpath('ocr', 'td[4]/text()')
                loader.add_xpath('grade', 'td[5]/text()')
                loader.add_xpath('date', 'td[6]/text()')
                loader.add_xpath('teacher', 'td[7]/text()')
                loader.item['module'] = None
                yield loader.load_item()
            else:
                loader = ItemLoader(CompletedCourseItem(), selector=row)
                loader.add_xpath('code', 'td[1]/a/text()')
                loader.add_xpath('name', 'td[1]/text()[2]')
                loader.add_xpath('cr', 'td[2]/b/text()')
                loader.add_xpath('ocr', 'td[3]/b/text()')
                loader.add_xpath('grade', 'td[4]/text()')
                loader.add_xpath('date', 'td[5]/text()')
                loader.add_xpath('teacher', 'td[6]/text()')
                loader.item['module'] = current_module
                yield loader.load_item()

SPIDER = OodiSpider()
