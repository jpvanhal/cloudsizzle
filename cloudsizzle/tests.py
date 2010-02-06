import doctest
import unittest
from minimock import Mock, restore, TraceTracker, mock
from cloudsizzle import utils, kp, pool
from cloudsizzle.kp import MockSIBConnection, Triple, uri, literal

class SIBTestCase(unittest.TestCase):
    def setUp(self):
        self.tt = TraceTracker()
        self.sc = MockSIBConnection()
        mock('pool._pool')
        mock('pool._pool.acquire', tracker=self.tt, returns=self.sc)
        mock('pool._pool.release', tracker=self.tt)

        # Basic ontology
        self.sc.insert([
            Triple(
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')),
            Triple(
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://www.w3.org/2000/01/rdf-schema#Class')),
            Triple(
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'),
                uri('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
                uri('http://www.w3.org/2000/01/rdf-schema#Resource')),
            Triple(
                uri('http://www.w3.org/2000/01/rdf-schema#Resource'),
                uri('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
                uri('http://www.w3.org/2000/01/rdf-schema#Resource')),
            Triple(
                uri('http://www.w3.org/2000/01/rdf-schema#Class'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://www.w3.org/2000/01/rdf-schema#Class')),
            Triple(
                uri('http://www.w3.org/2000/01/rdf-schema#Class'),
                uri('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
                uri('http://www.w3.org/2000/01/rdf-schema#Resource')),
            Triple(
                uri('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')),
            Triple(
                uri('http://www.w3.org/2000/01/rdf-schema#label'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')),
        ])

        # People triples
        self.sc.insert([
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Person')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#website'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#username'),
                literal('testijannu15')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#updated_at'),
                literal('2009-08-14T15:04:46Z')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#status'),
                uri('http://cos.alpha.sizl.org/people#cb286efb-05ed-435a-87bf-3ac3263fd51d')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#cb286efb-05ed-435a-87bf-3ac3263fd51d'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Status')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#cb286efb-05ed-435a-87bf-3ac3263fd51d'),
                uri('http://cos.alpha.sizl.org/people#message'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people#cb286efb-05ed-435a-87bf-3ac3263fd51d'),
                uri('http://cos.alpha.sizl.org/people#changed'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#role'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#phone_number'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#name'),
                uri('http://cos.alpha.sizl.org/people#c811c0dd-2400-4bea-a89e-cc4d91af9380')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#c811c0dd-2400-4bea-a89e-cc4d91af9380'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Name')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#c811c0dd-2400-4bea-a89e-cc4d91af9380'),
                uri('http://cos.alpha.sizl.org/people#unstructured'),
                literal('Testi Jannu15')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#c811c0dd-2400-4bea-a89e-cc4d91af9380'),
                uri('http://cos.alpha.sizl.org/people#given_name'),
                literal('Testi')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#c811c0dd-2400-4bea-a89e-cc4d91af9380'),
                uri('http://cos.alpha.sizl.org/people#family_name'),
                literal('Jannu15')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#msn_nick'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#is_association'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#irc_nick'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#gender'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#description'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#birthdate'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#avatar'),
                uri('http://cos.alpha.sizl.org/people#d0b74e12-08df-4f2d-95c7-fef24a24d55e')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#d0b74e12-08df-4f2d-95c7-fef24a24d55e'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Avatar')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#d0b74e12-08df-4f2d-95c7-fef24a24d55e'),
                uri('http://cos.alpha.sizl.org/people#status'),
                literal('not_set')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#d0b74e12-08df-4f2d-95c7-fef24a24d55e'),
                uri('http://cos.alpha.sizl.org/people#link'),
                uri('http://cos.alpha.sizl.org/people#7502776b-5e2b-4b23-8851-1a1c8e402bb7')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#7502776b-5e2b-4b23-8851-1a1c8e402bb7'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Link')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#7502776b-5e2b-4b23-8851-1a1c8e402bb7'),
                uri('http://cos.alpha.sizl.org/people#rel'),
                literal('self')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#7502776b-5e2b-4b23-8851-1a1c8e402bb7'),
                uri('http://cos.alpha.sizl.org/people#href'),
                literal('/people/dn3FNGIomr3OicaaWPEYjL/@avatar')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#address'),
                None),
        ])

        self.sc.insert([
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Person')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#website'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#username'),
                literal('aaatest4ivid')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#updated_at'),
                literal('2009-11-13T13:55:53Z')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#status'),
                uri('http://cos.alpha.sizl.org/people#fd3f5275-e946-4d4d-b46a-bd87af0f9c64')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#fd3f5275-e946-4d4d-b46a-bd87af0f9c64'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Status')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#fd3f5275-e946-4d4d-b46a-bd87af0f9c64'),
                uri('http://cos.alpha.sizl.org/people#message'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people#fd3f5275-e946-4d4d-b46a-bd87af0f9c64'),
                uri('http://cos.alpha.sizl.org/people#changed'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#role'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#phone_number'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#name'),
                uri('http://cos.alpha.sizl.org/people#e1a92c6a-9566-4385-800b-8e1f59155b56')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#e1a92c6a-9566-4385-800b-8e1f59155b56'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Name')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#e1a92c6a-9566-4385-800b-8e1f59155b56'),
                uri('http://cos.alpha.sizl.org/people#unstructured'),
                literal('testi hemmo')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#e1a92c6a-9566-4385-800b-8e1f59155b56'),
                uri('http://cos.alpha.sizl.org/people#given_name'),
                literal('testi')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#e1a92c6a-9566-4385-800b-8e1f59155b56'),
                uri('http://cos.alpha.sizl.org/people#family_name'),
                literal('hemmo')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#msn_nick'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#is_association'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#irc_nick'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#gender'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#description'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#birthdate'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#avatar'),
                uri('http://cos.alpha.sizl.org/people#c1939e3f-c9da-45b1-abc7-0a5536e199ac')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#c1939e3f-c9da-45b1-abc7-0a5536e199ac'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Avatar')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#c1939e3f-c9da-45b1-abc7-0a5536e199ac'),
                uri('http://cos.alpha.sizl.org/people#status'),
                literal('not_set')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#c1939e3f-c9da-45b1-abc7-0a5536e199ac'),
                uri('http://cos.alpha.sizl.org/people#link'),
                uri('http://cos.alpha.sizl.org/people#ee8cc93a-6c09-4b3a-b5ca-b2e200c7780f')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#ee8cc93a-6c09-4b3a-b5ca-b2e200c7780f'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Link')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#ee8cc93a-6c09-4b3a-b5ca-b2e200c7780f'),
                uri('http://cos.alpha.sizl.org/people#rel'),
                literal('self')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#ee8cc93a-6c09-4b3a-b5ca-b2e200c7780f'),
                uri('http://cos.alpha.sizl.org/people#href'),
                literal('/people/bbYJ_80fWr3Om4aaWPEYjL/@avatar')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#bbYJ_80fWr3Om4aaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#address'),
                None)
        ])


    def tearDown(self):
        self.sc.triple_store.clear()
        restore()

class UtilsTestCase(SIBTestCase):
    def test_fetch_rdf_graph(self):
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
            'website': None
        }

        subject = 'http://cos.alpha.sizl.org/people/ID#dn3FNGIomr3OicaaWPEYjL'
        actual = utils.fetch_rdf_graph(subject)

        self.assertEqual(expected, actual)

def suite():
    import cloudsizzle.scrapers.tests as scrapers
    import cloudsizzle.api.tests as api

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilsTestCase, 'test'))
    suite.addTest(api.suite())
    suite.addTest(scrapers.suite())
    suite.addTest(
        doctest.DocTestSuite(utils, optionflags=doctest.NORMALIZE_WHITESPACE))
    suite.addTest(doctest.DocTestSuite(kp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
