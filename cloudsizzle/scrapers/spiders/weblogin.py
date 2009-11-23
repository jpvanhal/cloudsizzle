from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector

class WebloginSpider(BaseSpider):
    extra_domain_names = ['weblogin.tkk.fi', 'idp.tkk.fi']

    def start_requests(self):
        self.log("Inititiating login procedure...")
        yield Request(self.start_urls[0], callback=self.before_login,
            dont_filter=True)

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
        return FormRequest.from_response(response, callback=self.parse,
            dont_filter=True)

SPIDER = WebloginSpider()
