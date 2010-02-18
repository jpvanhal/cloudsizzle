# encoding: utf8

import unittest
import doctest
from cloudsizzle import api
from cloudsizzle.kp import Triple, uri
from cloudsizzle.tests import SIBTestCase


class PeopleAPITestCase(SIBTestCase):

    def test_get_friends_of_user_with_friends(self):
        self.sc.insert([
            Triple(
               uri('http://cos.alpha.sizl.org/people/ID#d-cfIOQH0r3RjGaaWPEYjL'),
               uri('http://cos.alpha.sizl.org/people#Friend'),
               uri('http://cos.alpha.sizl.org/people/ID#d8vrPqQH0r3QeEaaWPEYjL')),
           Triple(
               uri('http://cos.alpha.sizl.org/people/ID#d-cfIOQH0r3RjGaaWPEYjL'),
               uri('http://cos.alpha.sizl.org/people#Friend'),
               uri('http://cos.alpha.sizl.org/people/ID#d9JgtWQH0r3QBRaaWPEYjL')),
            Triple(
               uri('http://cos.alpha.sizl.org/people/ID#d-cfIOQH0r3RjGaaWPEYjL'),
               uri('http://cos.alpha.sizl.org/people#Friend'),
               uri('http://cos.alpha.sizl.org/people/ID#d81F3WQH0r3OK1aaWPEYjL'))
        ])
        friends = sorted(api.people.get_friends('d-cfIOQH0r3RjGaaWPEYjL'))
        expected = ['d81F3WQH0r3OK1aaWPEYjL', 'd8vrPqQH0r3QeEaaWPEYjL',
            'd9JgtWQH0r3QBRaaWPEYjL']
        self.assertEqual(expected, friends)

    def test_get_friends_of_a_lonely_user(self):
        # triple store is empty
        friends = api.people.get_friends('aQ0zwc2Pur3PwyaaWPEYjL')
        self.assertEqual(0, len(friends))

    def test_get_person(self):
        expected = {
            'address': None,
            'avatar': {
                'link': {
                    'href': '/people/dn3FNGIomr3OicaaWPEYjL/@avatar',
                    'rel': 'self'
                },
                'status': 'not_set'
            },
            'birthdate': None,
            'description': None,
            'gender': None,
            'irc_nick': None,
            'is_association': None,
            'msn_nick': None,
            'name': {
                'family_name': 'Jannu15',
                'given_name': 'Testi',
                'unstructured': 'Testi Jannu15'
            },
            'phone_number': None,
            'role': None,
            'status': {
                'changed': None,
                'message': None
            },
            'updated_at': '2009-08-14T15:04:46Z',
            'username': 'testijannu15',
            'user_id': 'dn3FNGIomr3OicaaWPEYjL',
            'website': None
        }

        uid = 'dn3FNGIomr3OicaaWPEYjL'
        actual = api.people.get(uid)

        self.assertEqual(expected, actual)

    def test_get_all_people(self):
        expected = [
            'bbYJ_80fWr3Om4aaWPEYjL',
            'c0OzVoMZ0r3yhJaaWPEYjL',
            'dn3FNGIomr3OicaaWPEYjL',
        ]
        user_ids = api.people.get_all()
        self.assertEqual(expected, sorted(user_ids))

    def test_search_people_with_query_in_username_and_realname(self):
        self.assertEqual(
            ['dn3FNGIomr3OicaaWPEYjL'],
            api.people.search('Jannu'))

    def test_search_people_with_query_only_in_username(self):
        self.assertEqual(
            ['bbYJ_80fWr3Om4aaWPEYjL'],
            api.people.search('test4'))

    def test_search_people_with_query_only_in_realname(self):
        self.assertEqual(
            ['bbYJ_80fWr3Om4aaWPEYjL'],
            api.people.search('hemmo'))

    def test_search_people_with_no_matches(self):
        self.assertEqual([], api.people.search('ei ooo'))

    def test_search_people_with_unicode_query(self):
        self.assertEqual(
            ['c0OzVoMZ0r3yhJaaWPEYjL'],
            api.people.search(u'SEPPÄlä'))


class CourseAPITestCase(SIBTestCase):

    def test_search_exact_course_code(self):
        result = api.course.search(u'T-106.1003')
        self.assertEqual(['T-106.1003'], result)


    def test_search_case_insensitive_course_code(self):
        result = api.course.search(u't-106.1003')
        self.assertEqual(['T-106.1003'], result)


    def test_search_partial_course_code(self):
        result = api.course.search(u'T-106')
        expected = ['T-106.1003', 'T-106.1041', 'T-106.1043', 'T-106.1061']
        self.assertEqual(expected, result)


    def test_search_exact_course_name(self):
        result = api.course.search(u'Tietotekniikan työkurssi')
        self.assertEqual(['T-106.1061'], result)


    def test_search_partial_course_name(self):
        result = api.course.search(u'työkurssi')
        self.assertEqual(['T-106.1061'], result)


    def test_search_case_insensitive_and_partial_course_name(self):
        result = api.course.search(u'TYÖkUrssi')
        self.assertEqual(['T-106.1061'], result)


    def test_search_does_not_find_departments_or_faculties(self):
        result = api.course.search(u'Deparment')
        self.assertEqual(0, len(result))
        result = api.course.search(u'Faculty')
        self.assertEqual(0, len(result))


    def test_get_course(self):
        expected = {
            'code': 'T-106.1003',
            'name': 'IT Services at TKK',
            'department': 'T3050',
            'study_materials': 'Lecture notes, manuals.',
            'content': 'Basic computer terminology. Use of common ' \
                'applications in Unix, WWW and MS Windows environments.',
            'teaching_period': 'I (Autumn)',
            'extent': '2',
            'faculty': 'il',
            'department': 'T3050',
            'learning_outcomes': 'Having completed this course you are ' \
                'familiar with the use of information systems at Helsinki ' \
                'University of Technology.',
            'prerequisites': 'None.',
        }
        actual = api.course.get_course('T-106.1003')
        self.assertEqual(expected, actual)


    def test_get_course_raises_exception_with_invalid_code(self):
        self.assertRaises(Exception, api.course.get_course, 'foobar')


    def test_get_courses_by_department(self):
        courses = api.course.get_courses_by_department('T3050')
        self.assertEqual(5, len(courses))
        self.assertEqual('T-0.7050', courses[0]['code'])
        self.assertEqual('T-106.1061', courses[4]['code'])


    def test_get_departments_by_faculty(self):
        expected = [
            {
                'code': 'IL-0',
                'name': 'Common courses for the faculty',
            },
            {
                'code': 'T3010',
                'name': 'Department of Biomedical Engineering and Computational Science',
            },
            {
                'code': 'T3020',
                'name': 'Department of Mathematics and Systems Analysis',
            },
            {
                'code': 'T3030',
                'name': 'Department of Media Technology',
            },
            {
                'code': 'T3040',
                'name': 'Department of Engineering Physics',
            },
            {
                'code': 'T3050',
                'name': 'Department of Computer Science and Engineering',
            },
            {
                'code': 'T3060',
                'name': 'Department of Information and Computer Science',
            },
            {
                'code': 'T3070',
                'name': 'Department of Industrial Engineering and Management',
            },
            {
                'code': 'T3080',
                'name': 'BIT Research Centre',
            },
            {
                'code': 'T3090',
                'name': 'Language Centre',
            },
        ]
        actual = api.course.get_departments_by_faculty('il')
        self.assertEqual(expected, actual)


    def test_get_faculties(self):
        expected = [
            {
                'code': 'eri',
                'name': 'Other separate courses',
            },
            {
                'code': 'eta',
                'name': 'Faculty of Electronics, Communications and Automation',
            },
            {
                'code': 'ia',
                'name': 'Faculty of Engineering and Architecture',
            },
            {
                'code': 'il',
                'name': 'Faculty of Information and Natural Sciences',
            },
            {
                'code': 'km',
                'name': 'Faculty of Chemistry and Materials Sciences',
            },
        ]
        actual = api.course.get_faculties()
        self.assertEqual(expected, actual)


    def test_get_department_info(self):
        expected = {
            'code': 'T3050',
            'name': 'Department of Computer Science and Engineering',
        }
        actual = api.course.get_department_info('T3050')
        self.assertEqual(expected, actual)


    def test_get_department_info_raises_exception_with_invalid_code(self):
        self.assertRaises(Exception, api.course.get_department_info, 'foobar')


    def test_get_faculty_info(self):
        expected = {
            'code': 'il',
            'name': 'Faculty of Information and Natural Sciences',
        }
        actual = api.course.get_faculty_info('il')
        self.assertEqual(expected, actual)


    def test_get_faculty_info_raises_exception_with_invalid_code(self):
        self.assertRaises(Exception, api.course.get_faculty_info, 'foobar')

class SessionAPITestCase(SIBTestCase):
    def setUp(self):
        super(SessionAPITestCase, self).setUp()
        self.session = api.Session(username='pihina1', password='sala1')
        # Skip logging in with ASI
        self.session.user_id = 'd7TllUbOar34UjaaWPEYjL'

    def test_get_completed_courses(self):
        actual = self.session.get_completed_courses()
        expected = [
            {
                'code': 'T-106.5600',
                'name': 'Concurrent Programming P',
                'teacher': 'Heikki Saikkonen',
                'date': '2009-12-21',
                'grade': '5',
                'cr': '5',
            },
            {
                'code': 'Mat-1.401',
                'name': 'Basic Course in Mathematics L 1',
                'teacher': 'Juhani Pitkäranta',
                'date': '2004-12-14',
                'grade': '2',
                'ocr': '6',
            },
        ]
        self.assertEqual(expected, actual)

    def test_is_completed_course(self):
        self.assertTrue(self.session.is_completed_course('T-106.5600') is True)
        self.assertTrue(self.session.is_completed_course('Mat-1.401') is True)
        self.assertTrue(self.session.is_completed_course('T-106.1003') is False)
        self.assertTrue(self.session.is_completed_course('foobar') is False)
        self.assertTrue(self.session.is_completed_course('') is False)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(PeopleAPITestCase, 'test'))
    test_suite.addTest(unittest.makeSuite(CourseAPITestCase, 'test'))
    test_suite.addTest(unittest.makeSuite(SessionAPITestCase, 'test'))
    for module in (api.course, api.people, api.session):
        test_suite.addTest(doctest.DocTestSuite(module,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
