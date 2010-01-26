import os
from scrapy.http import HtmlResponse, Request

class MockResponseFactory(object):
    def __init__(self, directory):
        self.directory = directory

    def create_response(self, url, filename):
        filename = os.path.join(self.directory, 'sample_data', filename)
        response = HtmlResponse(url, body=open(filename).read())
        response.request = Request(url)
        return response
