from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector

class OodiSpider(CrawlSpider):
    domain_name = 'oodi.tkk.fi'
    start_urls = ['https://oodi.tkk.fi/w/oodishibboleth.jsp']
    extra_domain_names = ['weblogin.tkk.fi', 'idp.tkk.fi']

    rules = (
        Rule(
            SgmlLinkExtractor(
                allow=r'/w/valikko\.jsp',
                tags='frame', attrs=('src', )),
            callback='parse_menu'
        ),
    )

    def start_requests(self):
        self.log("Inititiating login procedure...")
        yield Request("https://oodi.tkk.fi/w/oodishibboleth.jsp",
                      callback=self.before_login, dont_filter=True)

    def before_login(self, response):
        self.log("Clicking continue...")
        return FormRequest.from_response(response, callback=self.login,
            dont_filter=True)

    def login(self, response):
        self.log("Filling login form...")
        USERNAME = raw_input("Username: ")
        PASSWORD = raw_input("Password: ")
        return FormRequest.from_response(response,
            formdata={'user': USERNAME, 'pass': PASSWORD},
            callback=self.after_login, dont_filter=True)

    def after_login(self, response):
        if "authentication failed" in response.body:
            self.log("Authentication failed!", "ERROR")
            return
        self.log("Authentication succesful!")
        self.log("Clicking continue again...")
        return FormRequest.from_response(response, callback=self.after_login2,
            dont_filter=True)

    def after_login2(self, response):
        self.log("Clicking continue the third time....")
        return FormRequest.from_response(response, callback=self.after_login3,
            dont_filter=True)

    def after_login3(self, response):
        assert response.url == "https://oodi.tkk.fi/w/oodishibboleth.jsp"
        self.log("Logged in!")
        extractor = SgmlLinkExtractor(allow=r'/w/valikko\.jsp', tags='frame', attrs=('src', ))
        link = extractor.extract_links(response)[0]
        return Request(link.url, callback=self.parse_menu)

    def parse_menu(self, response):
        self.log(response.url)
        hxs = HtmlXPathSelector(response)
        name, student_number = hxs.select('//td[@class="valikkonimi"]/text()').extract()
        print name
        print student_number

SPIDER = OodiSpider()
