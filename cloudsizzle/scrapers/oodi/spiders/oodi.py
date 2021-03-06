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

import urllib
import urlparse
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from cloudsizzle.scrapers.spiders.weblogin import WebloginSpider
from cloudsizzle.scrapers.oodi.items import CompletedCourseItem, ModuleItem
from cloudsizzle.scrapers.items import ItemLoader


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
        completed_studies_url = 'https://oodi.tkk.fi/w/omatopinn.jsp?' + params
        yield Request(
            url=completed_studies_url,
            callback=self.parse_completed_studies)

    def parse_session_hash(self, response):
        extractor = SgmlLinkExtractor(
            allow=r'/w/valikko\.jsp', tags='frame', attrs=('src', ))
        link = extractor.extract_links(response)[0]
        query = urlparse.urlparse(link.url).query
        params = urlparse.parse_qs(query)
        return params['MD5avain'][0]

    def parse_completed_studies(self, response):
        hxs = HtmlXPathSelector(response)
        current_module = None
        for row in hxs.select('//table[@class="eisei"]/tbody/tr[td]'):
            is_module = row.select('td/a/img')
            is_ungrouped_course = row.select(
                'td[@class="tyyli0" or @class="tyyli1"]')
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
