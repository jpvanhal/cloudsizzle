import unittest
from cloudsizzle.scrapers.noppa.spiders.tests import noppa

def suite():
    suite = unittest.TestSuite()
    suite.addTest(noppa.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
