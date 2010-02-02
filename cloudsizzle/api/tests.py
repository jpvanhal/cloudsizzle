import unittest
import doctest
from cloudsizzle.api import course, people, session
from minimock import Mock, restore, TraceTracker
from cloudsizzle import pool
from cloudsizzle.kp import Triple, uri, literal

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.tt = TraceTracker()
        self.sc = Mock('SIBConnection', tracker=self.tt)
        pool._pool = Mock('ConnectionPool')
        pool._pool.acquire = Mock('ConnectionPool.acquire', tracker=self.tt,
            returns=self.sc)
        pool._pool.release = Mock('ConnectionPool.release', tracker=self.tt)

    def tearDown(self):
        restore()

class PeopleGetFriendsTestCase(APITestCase):
    BASE_URI = 'http://cloudsizzle.cs.hut.fi/onto/people/'

    def test_get_friends_of_user_with_friends(self):
        self.sc.query = Mock('SIBConnection.query', tracker=self.tt, returns=[
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
        self.tt.check("Called ConnectionPool.acquire()")
        self.tt.check("Called SIBConnection.query(" \
            "Triple(uri('" + self.BASE_URI + "d-cfIOQH0r3RjGaaWPEYjL'), " \
            "uri('has_friend'), None))")
        self.tt.check(
            "Called ConnectionPool.release(<Mock 0x... SIBConnection>)")
        expected = ['d81F3WQH0r3OK1aaWPEYjL', 'd8vrPqQH0r3QeEaaWPEYjL',
            'd9JgtWQH0r3QBRaaWPEYjL']
        self.assertEqual(expected, friends)

    def test_get_friends_of_a_lonely_user(self):
        self.sc.query = Mock('SIBConnection.query', tracker=self.tt, returns=[])
        friends = people.get_friends('aQ0zwc2Pur3PwyaaWPEYjL')
        self.tt.check("Called ConnectionPool.acquire()")
        self.tt.check("Called SIBConnection.query(" \
            "Triple(uri('" + self.BASE_URI + "aQ0zwc2Pur3PwyaaWPEYjL'), "\
            "uri('has_friend'), None))")
        self.tt.check(
            "Called ConnectionPool.release(<Mock 0x... SIBConnection>)")
        self.assertEqual(0, len(friends))

class PeopleSearchTestCase(APITestCase):
    def test_search(self):
        self.sc.query = Mock('SIBConnection.query', tracker=self.tt,
            returns_iter=[[
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
                    literal('kafka'))],
                [
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
                    literal('Franz Kafka'))]
        ])
        user_ids = sorted(people.search('Pang'))
        expected = ['aQ0zwc2Pur3PwyaaWPEYjL', 'bG1oHm3yWr3RiVaaWPEYjL',
            'bKBrQM27er3PeAaaWPEYjL']
        self.tt.check('Called ConnectionPool.acquire()')
        self.tt.check("Called SIBConnection.query("\
            "Triple(None, uri('http://cos.alpha.sizl.org/people#username'),"\
                "None))")
        self.tt.check("Called SIBConnection.query("\
            "Triple(None, uri('http://cos.alpha.sizl.org/people#name'), None))")
        self.tt.check("Called ConnectionPool.release(<Mock 0x... SIBConnection>)")
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
