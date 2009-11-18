import os

from scrapy.http import HtmlResponse

class MockResponse(HtmlResponse):
    def __init__(self, url, filename):
        filename = os.path.join(os.path.dirname(__file__), filename)
        HtmlResponse.__init__(self, url, body=open(filename).read())
