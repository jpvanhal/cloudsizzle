# encoding: utf8

import doctest
import unittest
from minimock import restore, TraceTracker, mock
from cloudsizzle import utils, kp, pool
from cloudsizzle.kp import MockSIBConnection, Triple, uri, literal

class SIBTestCase(unittest.TestCase):
    def setUp(self):
        self.trace_tracker = TraceTracker()
        self.sc = MockSIBConnection()
        mock('pool.POOL')
        mock('pool.POOL.acquire', tracker=self.trace_tracker, returns=self.sc)
        mock('pool.POOL.release', tracker=self.trace_tracker)

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
        self.sc.insert([
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#c0OzVoMZ0r3yhJaaWPEYjL'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Person')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#c0OzVoMZ0r3yhJaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#username'),
                literal('lassi')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#c0OzVoMZ0r3yhJaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#updated_at'),
                literal('2010-01-08T08:57:54Z')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#c0OzVoMZ0r3yhJaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#role'),
                None),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#c0OzVoMZ0r3yhJaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#name'),
                uri('http://cos.alpha.sizl.org/people#5aa1b375-c422-4829-96f9-14ad2a04544f')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#5aa1b375-c422-4829-96f9-14ad2a04544f'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                uri('http://cos.alpha.sizl.org/people#Name')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#5aa1b375-c422-4829-96f9-14ad2a04544f'),
                uri('http://cos.alpha.sizl.org/people#unstructured'),
                literal('Lassi Seppälä')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#5aa1b375-c422-4829-96f9-14ad2a04544f'),
                uri('http://cos.alpha.sizl.org/people#given_name'),
                literal('Lassi')),
            Triple(
                uri('http://cos.alpha.sizl.org/people#5aa1b375-c422-4829-96f9-14ad2a04544f'),
                uri('http://cos.alpha.sizl.org/people#family_name'),
                literal('Seppälä')),
            Triple(
                uri('http://cos.alpha.sizl.org/people/ID#c0OzVoMZ0r3yhJaaWPEYjL'),
                uri('http://cos.alpha.sizl.org/people#is_association'),
                None),
            ])

        # Course information
        self.sc.insert([
            Triple(
                uri('eri'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Faculty')),
            Triple(
                uri('eri'),
                uri('name'),
                literal('Other separate courses')),
            Triple(
                uri('eta'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Faculty')),
            Triple(
                uri('eta'),
                uri('name'),
                literal('Faculty of Electronics, Communications and Automation')),
            Triple(
                uri('ia'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Faculty')),
            Triple(
                uri('ia'),
                uri('name'),
                literal('Faculty of Engineering and Architecture')),
            Triple(
                uri('il'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Faculty')),
            Triple(
                uri('il'),
                uri('name'),
                literal('Faculty of Information and Natural Sciences')),
            Triple(
                uri('km'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Faculty')),
            Triple(
                uri('km'),
                uri('name'),
                literal('Faculty of Chemistry and Materials Sciences')),

            Triple(
                uri('IL-0'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('IL-0'),
                uri('name'),
                literal('Common courses for the faculty')),
            Triple(
                uri('IL-0'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3010'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3010'),
                uri('name'),
                literal('Department of Biomedical Engineering and Computational Science')),
            Triple(
                uri('T3010'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3020'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3020'),
                uri('name'),
                literal('Department of Mathematics and Systems Analysis')),
            Triple(
                uri('T3020'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3030'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3030'),
                uri('name'),
                literal('Department of Media Technology')),
            Triple(
                uri('T3030'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3040'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3040'),
                uri('name'),
                literal('Department of Engineering Physics')),
            Triple(
                uri('T3040'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3050'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3050'),
                uri('name'),
                literal('Department of Computer Science and Engineering')),
            Triple(
                uri('T3050'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3060'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3060'),
                uri('name'),
                literal('Department of Information and Computer Science')),
            Triple(
                uri('T3060'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3070'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3070'),
                uri('name'),
                literal('Department of Industrial Engineering and Management')),
            Triple(
                uri('T3070'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3080'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3080'),
                uri('name'),
                literal('BIT Research Centre')),
            Triple(
                uri('T3080'),
                uri('faculty'),
                uri('il')),
            Triple(
                uri('T3090'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Department')),
            Triple(
                uri('T3090'),
                uri('name'),
                literal('Language Centre')),
            Triple(
                uri('T3090'),
                uri('faculty'),
                uri('il')),

            Triple(
                uri('T-0.7050'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Course')),
            Triple(
                uri('T-0.7050'),
                uri('name'),
                literal('Introduction to Postgraduate Studies in Computer Science P')),
            Triple(
                uri('T-0.7050'),
                uri('department'),
                uri('T3050')),
            Triple(
                uri('T-0.7050'),
                uri('content'),
                literal('Basic research skills. The publishing process. Scientific presentations. Research areas in computer science.')),
            Triple(
                uri('T-0.7050'),
                uri('teaching_period'),
                literal('III-IV')),
            Triple(
                uri('T-0.7050'),
                uri('extent'),
                literal('2')),
            Triple(
                uri('T-0.7050'),
                uri('learning_outcomes'),
                literal('PProvide a basic understanding of the scientific process and of the research paradigms relevant to research. Provide guidelines and support for planning the Ph.D. work. Provide an understanding and experience of the publishing and peer-review process in the field.')),
            Triple(
                uri('T-106.1003'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Course')),
            Triple(
                uri('T-106.1003'),
                uri('name'),
                literal('IT Services at TKK')),
            Triple(
                uri('T-106.1003'),
                uri('department'),
                uri('T3050')),
            Triple(
                uri('T-106.1003'),
                uri('study_materials'),
                literal('Lecture notes, manuals.')),
            Triple(
                uri('T-106.1003'),
                uri('content'),
                literal('Basic computer terminology. Use of common applications in Unix, WWW and MS Windows environments.')),
            Triple(
                uri('T-106.1003'),
                uri('teaching_period'),
                literal('I (Autumn)')),
            Triple(
                uri('T-106.1003'),
                uri('extent'),
                literal('2')),
            Triple(
                uri('T-106.1003'),
                uri('learning_outcomes'),
                literal('Having completed this course you are familiar with the use of information systems at Helsinki University of Technology.')),
            Triple(
                uri('T-106.1003'),
                uri('prerequisites'),
                literal('None.')),
            Triple(
                uri('T-106.1041'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Course')),
            Triple(
                uri('T-106.1041'),
                uri('name'),
                literal('Tietotekniikan peruskurssi')),
            Triple(
                uri('T-106.1041'),
                uri('department'),
                uri('T3050')),
            Triple(
                uri('T-106.1041'),
                uri('study_materials'),
                literal('Luentomateriaali, nopassa jaettava materiaali')),
            Triple(
                uri('T-106.1041'),
                uri('content'),
                literal('Yleissivistävä katsaus tietotekniikan eri aihealueisiin.')),
            Triple(
                uri('T-106.1041'),
                uri('teaching_period'),
                literal('I - II')),
            Triple(
                uri('T-106.1041'),
                uri('extent'),
                literal('3')),
            Triple(
                uri('T-106.1041'),
                uri('learning_outcomes'),
                literal('Tietotekniikan keskeisten osa-alueiden tuntemus.')),
            Triple(
                uri('T-106.1041'),
                uri('prerequisites'),
                literal('Ei vaadita.')),
            Triple(
                uri('T-106.1043'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Course')),
            Triple(
                uri('T-106.1043'),
                uri('name'),
                literal('Information Technology - Basic Course')),
            Triple(
                uri('T-106.1043'),
                uri('department'),
                uri('T3050')),
            Triple(
                uri('T-106.1043'),
                uri('study_materials'),
                literal('Reed, David: "A Balanced Introduction to Computer Science" (2nd edition). Pearson Education, Upper Saddle River (NJ), Pearson Prentice Hall, ISBN 0-13-601722-3')),
            Triple(
                uri('T-106.1043'),
                uri('content'),
                literal('Computer science basics.')),
            Triple(
                uri('T-106.1043'),
                uri('teaching_period'),
                literal('I - II (Autumn)')),
            Triple(
                uri('T-106.1043'),
                uri('extent'),
                literal('3')),
            Triple(
                uri('T-106.1043'),
                uri('learning_outcomes'),
                literal('Having completed this course you are familiar with essential fields of computer science.')),
            Triple(
                uri('T-106.1043'),
                uri('prerequisites'),
                None),
            Triple(
                uri('T-106.1061'),
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('Course')),
            Triple(
                uri('T-106.1061'),
                uri('name'),
                literal('Tietotekniikan työkurssi')),
            Triple(
                uri('T-106.1061'),
                uri('department'),
                uri('T3050')),
            Triple(
                uri('T-106.1061'),
                uri('study_materials'),
                literal('Ilmoitetaan kurssin Noppa-sivulla: https://noppa.tkk.fi/noppa/kurssi/t-1... .')),
            Triple(
                uri('T-106.1061'),
                uri('content'),
                literal('Opiskelussa ja työelämässä yleisesti käytetyt toimistotyökalut, WWW-sivujen laatiminen ja ohjelmoinnin alkeet.')),
            Triple(
                uri('T-106.1061'),
                uri('teaching_period'),
                literal('III - IV')),
            Triple(
                uri('T-106.1061'),
                uri('extent'),
                literal('3')),
            Triple(
                uri('T-106.1061'),
                uri('learning_outcomes'),
                literal('Osaat käyttää monipuolisesti ja tehokkaasti opiskelu- ja työelämässä yleisesti käytettyjä toimistotyökaluja. Hallitset WWW-sivujen laatimisen sekä ohjelmoinnin alkeet.')),
            Triple(
                uri('T-106.1061'),
                uri('prerequisites'),
                literal('Ei vaadita.')),
        ])

        # Completed courses
        subject = uri('http://cloudsizzle.cs.hut.fi/ontology/people/d7TllUbOar34UjaaWPEYjL/courses/completed/T-106.5600')
        self.sc.insert([
            Triple(
                subject,
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('CompletedCourse')),
            Triple(
                subject,
                uri('name'),
                literal('Concurrent Programming P')),
            Triple(
                subject,
                uri('teacher'),
                literal('Heikki Saikkonen')),
            Triple(
                subject,
                uri('date'),
                literal('2009-12-21')),
            Triple(
                subject,
                uri('grade'),
                literal('5')),
            Triple(
                subject,
                uri('cr'),
                literal('5')),
            Triple(
                subject,
                uri('code'),
                literal('T-106.5600')),
            Triple(
                subject,
                uri('user'),
                uri('http://cos.alpha.sizl.org/people/ID#d7TllUbOar34UjaaWPEYjL')),
        ])
        subject = uri('http://cloudsizzle.cs.hut.fi/ontology/people/d7TllUbOar34UjaaWPEYjL/courses/completed/Mat-1.401')
        self.sc.insert([
            Triple(
                subject,
                uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                literal('CompletedCourse')),
            Triple(
                subject,
                uri('name'),
                literal('Basic Course in Mathematics L 1')),
            Triple(
                subject,
                uri('teacher'),
                literal('Juhani Pitkäranta')),
            Triple(
                subject,
                uri('date'),
                literal('2004-12-14')),
            Triple(
                subject,
                uri('grade'),
                literal('2')),
            Triple(
                subject,
                uri('code'),
                literal('Mat-1.401')),
            Triple(
                subject,
                uri('ocr'),
                literal('6')),
            Triple(
                subject,
                uri('user'),
                uri('http://cos.alpha.sizl.org/people/ID#d7TllUbOar34UjaaWPEYjL'))
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

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(UtilsTestCase, 'test'))
    test_suite.addTest(api.suite())
    test_suite.addTest(scrapers.suite())
    test_suite.addTest(
        doctest.DocTestSuite(utils, optionflags=doctest.NORMALIZE_WHITESPACE))
    test_suite.addTest(doctest.DocTestSuite(kp))
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
