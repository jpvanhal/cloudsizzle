import unittest
from cloudsizzle.scrapers.tests import pipelines
from cloudsizzle.scrapers.spiders import tests as spiders

def suite():
    suite = unittest.TestSuite()
    suite.addTest(pipelines.suite())
    suite.addTest(spiders.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
