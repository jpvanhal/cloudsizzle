import unittest
from cloudsizzle.scrapers.oodi.spiders.tests import oodi

def suite():
    suite = unittest.TestSuite()
    suite.addTest(oodi.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')