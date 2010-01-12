import unittest
from cloudsizzle.scrapers.noppa import tests as noppa
from cloudsizzle.scrapers.oodi import tests as oodi

def suite():
    suite = unittest.TestSuite()
    suite.addTest(noppa.suite())
    suite.addTest(oodi.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
