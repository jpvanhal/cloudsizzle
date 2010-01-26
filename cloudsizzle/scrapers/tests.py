import unittest
import cloudsizzle.scrapers.noppa.tests as noppa
import cloudsizzle.scrapers.oodi.tests as oodi

def suite():
    suite = unittest.TestSuite()
    suite.addTest(noppa.suite())
    suite.addTest(oodi.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
