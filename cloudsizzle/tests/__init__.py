import unittest
from cloudsizzle.scrapers import tests as scrapers

def suite():
    suite = unittest.TestSuite()
    suite.addTest(scrapers.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
