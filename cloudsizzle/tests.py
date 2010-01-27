import unittest
import doctest
from cloudsizzle.scrapers import tests as scrapers
from cloudsizzle import utils
from cloudsizzle import kp

def suite():
    suite = unittest.TestSuite()
    suite.addTest(scrapers.suite())
    suite.addTest(doctest.DocTestSuite(utils))
    suite.addTest(doctest.DocTestSuite(kp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
