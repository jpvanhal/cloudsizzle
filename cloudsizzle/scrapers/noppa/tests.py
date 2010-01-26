import unittest
import cloudsizzle.scrapers.noppa.spiders.tests as spiders

def suite():
    suite = unittest.TestSuite()
    suite.addTest(spiders.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
