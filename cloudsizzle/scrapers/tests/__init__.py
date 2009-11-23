import unittest
from cloudsizzle.scrapers.tests import noppa, oodi

def suite():
    suite = unittest.TestSuite()
    suite.addTest(noppa.suite())
    suite.addTest(oodi.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
