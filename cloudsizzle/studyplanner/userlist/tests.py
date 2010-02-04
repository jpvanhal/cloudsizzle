from cloudsizzle.studyplanner import testhelp
import unittest

class ValidationTest(unittest.TestCase):

    def test_validity(self):

        res = testhelp.validate_html('/users/')
        
        self.failIfEqual(False,res[0],res[1])
