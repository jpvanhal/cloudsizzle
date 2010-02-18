import unittest
import cloudsizzle.scrapers.noppa.spiders.tests as spiders


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(spiders.suite())
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
