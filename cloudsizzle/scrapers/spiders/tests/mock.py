import os

from scrapy.http import HtmlResponse, Request

class MockResponse(HtmlResponse):
    def __init__(self, url, filename):
        filename = os.path.join(os.path.dirname(__file__), 'sample_data', filename)
        HtmlResponse.__init__(self, url, body=open(filename).read())
        self.request = Request(url)
