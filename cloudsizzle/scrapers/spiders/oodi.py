from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider

USERNAME = "user"
PASSWORD = "secret"

class OodiSpider(BaseSpider):
    domain_name = 'oodi.tkk.fi'
    start_urls = ['https://oodi.tkk.fi/']
    extra_domain_names = ['weblogin.tkk.fi', 'idp.tkk.fi']

    def start_requests(self):
        yield Request("https://oodi.tkk.fi/w/oodishibboleth.jsp",
                            callback=self.before_login)

    def before_login(self, response):
        print response.url
        print "Clicking continue"
        return FormRequest.from_response(response, callback=self.login)

    def login(self, response):
        assert response.url == "https://weblogin.tkk.fi/app/login"
        print response.url
        print "Filling login form"
        return FormRequest.from_response(response,
            formdata={'user': USERNAME, 'pass': PASSWORD},
            callback=self.after_login)

    def after_login(self, response):
        print response.url
        if "authentication failed" in response.body:
            self.log("ERROR: authentication failed")
            return
        print "Clicking continue"
        return FormRequest.from_response(response, callback=self.after_login2)

    def after_login2(self, response):
        print response.url


SPIDER = OodiSpider()
