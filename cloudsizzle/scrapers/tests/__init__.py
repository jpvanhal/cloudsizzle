import unittest
from cloudsizzle.scrapers.tests import noppa

def suite():
    suite = unittest.TestSuite()
    suite.addTest(noppa.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
