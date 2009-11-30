# coding=utf-8
import unittest
from scrapy.item import Item, Field
from cloudsizzle.scrapers.pipelines import UTF8Pipeline

class TestItem(Item):
    foo = Field()

class UTF8PipelineTestCase(unittest.TestCase):
    def setUp(self):
        self.item = TestItem()
        self.pipeline = UTF8Pipeline()

    def test_encodes_unicode_strings_to_utf8(self):
        self.item['foo'] = u'ä'
        processed = self.pipeline.process_item('', self.item)
        self.assertEqual('\xc3\xa4', processed['foo'])

    def test_encode_normal_strings_to_utf8(self):
        self.item['foo'] = 'ä'
        processed = self.pipeline.process_item('', self.item)
        self.assertEqual('\xc3\xa4', processed['foo'])

    def test_objects_other_than_strings_are_not_touched(self):
        self.item['foo'] = 5
        processed = self.pipeline.process_item('', self.item)
        self.assertEqual(5, processed['foo'])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UTF8PipelineTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
