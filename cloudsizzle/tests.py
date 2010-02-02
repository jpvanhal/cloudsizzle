import unittest
import doctest
import cloudsizzle.scrapers.tests as scrapers
from cloudsizzle import utils
from cloudsizzle import kp
import cloudsizzle.api.tests as api

def suite():
    suite = unittest.TestSuite()
    suite.addTest(api.suite())
    suite.addTest(scrapers.suite())
    suite.addTest(
        doctest.DocTestSuite(utils, optionflags=doctest.NORMALIZE_WHITESPACE))
    suite.addTest(doctest.DocTestSuite(kp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
