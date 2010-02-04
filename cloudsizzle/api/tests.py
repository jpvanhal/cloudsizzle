import unittest
import doctest
from cloudsizzle.api import course, people, session
from cloudsizzle import pool
from cloudsizzle.kp import Triple, uri, literal
from cloudsizzle.tests import SIBTestCase

class PeopleGetFriendsTestCase(SIBTestCase):
    BASE_URI = 'http://cloudsizzle.cs.hut.fi/onto/people/'

    def test_get_friends_of_user_with_friends(self):
        self.sc.insert([
            Triple(
               uri(self.BASE_URI + 'd-cfIOQH0r3RjGaaWPEYjL'),
               uri('has_friend'),
               literal(self.BASE_URI + 'd8vrPqQH0r3QeEaaWPEYjL')),
           Triple(
               uri(self.BASE_URI + 'd-cfIOQH0r3RjGaaWPEYjL'),
               uri('has_friend'),
               literal(self.BASE_URI + 'd9JgtWQH0r3QBRaaWPEYjL')),
            Triple(
               uri(self.BASE_URI + 'd-cfIOQH0r3RjGaaWPEYjL'),
               uri('has_friend'),
               literal(self.BASE_URI + 'd81F3WQH0r3OK1aaWPEYjL'))
        ])
        friends = sorted(people.get_friends('d-cfIOQH0r3RjGaaWPEYjL'))
        expected = ['d81F3WQH0r3OK1aaWPEYjL', 'd8vrPqQH0r3QeEaaWPEYjL',
            'd9JgtWQH0r3QBRaaWPEYjL']
        self.assertEqual(expected, friends)

    def test_get_friends_of_a_lonely_user(self):
        # triple store is empty
        friends = people.get_friends('aQ0zwc2Pur3PwyaaWPEYjL')
        self.assertEqual(0, len(friends))

class PeopleSearchTestCase(SIBTestCase):
    def test_search(self):
        self.sc.insert([
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#aQ0zwc2Pur3PwyaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#username'),
                literal('pangbo')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bKBrQM27er3PeAaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#username'),
                literal('geeman')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bG1oHm3yWr3RiVaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#username'),
                literal('pang')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#cZIUMG870r3P1-aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#username'),
                literal('kafka')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#aQ0zwc2Pur3PwyaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#name'),
                literal('Pang Bo')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bKBrQM27er3PeAaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#name'),
                literal('bo pang')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bG1oHm3yWr3RiVaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#name'),
                literal('None')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#cZIUMG870r3P1-aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#name'),
                literal('Franz Kafka')),
        ])
        user_ids = sorted(people.search('Pang'))
        expected = ['aQ0zwc2Pur3PwyaaWPEYjL', 'bG1oHm3yWr3RiVaaWPEYjL',
            'bKBrQM27er3PeAaaWPEYjL']
        self.assertEqual(expected, user_ids)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PeopleGetFriendsTestCase, 'test'))
    suite.addTest(unittest.makeSuite(PeopleSearchTestCase, 'test'))
    for module in (course, people, session):
        suite.addTest(doctest.DocTestSuite(module,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
