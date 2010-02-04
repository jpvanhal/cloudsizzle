import unittest
import doctest
from cloudsizzle.api import course, people, session
from cloudsizzle import pool
from cloudsizzle.kp import Triple, uri, literal
from cloudsizzle.tests import SIBTestCase

class PeopleAPITestCase(SIBTestCase):
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

    def test_get_person(self):
        expected = {
            'address': 'None',
            'avatar': {
                'link': {
                    'href': '/people/dn3FNGIomr3OicaaWPEYjL/@avatar',
                    'rel': 'self'
                },
                'status': 'not_set'
            },
            'birthdate': 'None',
            'description': 'None',
            'gender': 'None',
            'irc_nick': 'None',
            'is_association': 'None',
            'msn_nick': 'None',
            'name': {
                'family_name': 'Jannu15',
                'given_name': 'Testi',
                'unstructured': 'Testi Jannu15'
            },
            'phone_number': 'None',
            'role': 'None',
            'status': {
                'changed': 'None',
                'message': 'None'
            },
            'updated_at': '2009-08-14T15:04:46Z',
            'username': 'testijannu15',
            'website': 'None'
        }

        uid = 'dn3FNGIomr3OicaaWPEYjL'
        actual = people.get(uid)

        self.assertEqual(expected, actual)

    def test_get_all_people(self):
        expected = [
            'bbYJ_80fWr3Om4aaWPEYjL',
            'dn3FNGIomr3OicaaWPEYjL',
        ]
        user_ids = people.get_all()
        self.assertEqual(expected, sorted(user_ids))

    def test_search_people_with_query_in_username_and_realname(self):
        self.assertEqual(['dn3FNGIomr3OicaaWPEYjL'], people.search('Jannu'))

    def test_search_people_with_query_only_in_username(self):
        self.assertEqual(['bbYJ_80fWr3Om4aaWPEYjL'], people.search('test4'))

    def test_search_people_with_query_only_in_realname(self):
        self.assertEqual(['bbYJ_80fWr3Om4aaWPEYjL'], people.search('hemmo'))

    def test_search_people_with_no_matches(self):
        self.assertEqual([], people.search('ei ooo'))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PeopleAPITestCase, 'test'))
    for module in (course, people, session):
        suite.addTest(doctest.DocTestSuite(module,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
