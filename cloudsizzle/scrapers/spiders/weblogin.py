from getpass import getpass
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy import log

class WebloginSpider(BaseSpider):
    """Logs into web services that use TKK's Weblogin system.

    This class should not be instantiated directly, but extended by a spider
    that needs to authenticate with Weblogin.

    The user credentials that are used for logging in can be defined in
    Scrapy's settings (see cloudsizzle.scrapers.settings) or passed in as
    command line parameters when starting the spider. The settings are
    TKK_WEBLOGIN_USERNAME for the username and TKK_WEBLOGIN_PASSWORD for the
    password.

    """
    login_url = None
    extra_domain_names = ['weblogin.tkk.fi', 'idp.tkk.fi']

    def __init__(self):
        BaseSpider.__init__(self)

    def start_requests(self):
        self.log("Inititiating login procedure...")
        if self.login_url is None:
            raise Exception(
                "You must set the login_url class attribute that is the url " \
                "of the 'Login' link the user clicks.")
        yield Request(self.login_url, callback=self.redirect_to_login_form,
            dont_filter=True)

    def redirect_to_login_form(self, response):
        self.log("Clicking continue...")
        return FormRequest.from_response(response,
            callback=self.fill_login_form, dont_filter=True)

    def fill_login_form(self, response):
        self.log("Filling login form...")
        self.username = settings['TKK_WEBLOGIN_USERNAME']
        if not self.username:
            self.username = raw_input('TKK Weblogin username: ')
        self.password = settings['TKK_WEBLOGIN_PASSWORD']
        if not self.password:
            self.password = getpass('TKK Weblogin password: ')
        formdata = {
            'user': self.username,
            'pass': self.password
        }
        return FormRequest.from_response(response, formdata=formdata,
            callback=self.check_authentication_result, dont_filter=True)

    def check_authentication_result(self, response):
        if "Authentication Failed." in response.body:
            self.log("Authentication failed!", level=log.ERROR)
            return
        self.log("Authentication succesful!")
        self.log("Clicking continue again...")
        return FormRequest.from_response(response, callback=self.finish_login,
            dont_filter=True)

    def finish_login(self, response):
        self.log("Clicking continue the third time....")
        return FormRequest.from_response(response, callback=self.parse,
            dont_filter=True)
