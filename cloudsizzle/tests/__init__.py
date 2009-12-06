import unittest
import doctest
from cloudsizzle.scrapers import tests as scrapers
from cloudsizzle import utils

def suite():
    suite = unittest.TestSuite()
    suite.addTest(scrapers.suite())
    suite.addTest(doctest.DocTestSuite(utils))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
