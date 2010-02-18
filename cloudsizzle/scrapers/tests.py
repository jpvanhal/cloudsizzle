import unittest
import cloudsizzle.scrapers.noppa.tests as noppa
import cloudsizzle.scrapers.oodi.tests as oodi

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(noppa.suite())
    test_suite.addTest(oodi.suite())
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
