# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2010 CloudSizzle Team
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
Pipeline for storing scraped triples to SIB.

See: http://doc.scrapy.org/topics/item-pipeline.html

"""
from .items import FacultyItem, DepartmentItem, CourseItem, CourseOverviewItem
from cloudsizzle.kp import SIBConnection, Triple, uri


def transform_to_triples(item):
    if isinstance(item, FacultyItem):
        return [
            Triple(item['code'], 'rdf:type', 'Faculty'),
            Triple(item['code'], 'name', item['name'])]
    elif isinstance(item, DepartmentItem):
        return [
            Triple(item['code'], 'rdf:type', 'Department'),
            Triple(item['code'], 'name', item['name']),
            Triple(item['code'], 'faculty', uri(item['faculty']['code']))]
    elif isinstance(item, CourseItem):
        return [
            Triple(item['code'], 'rdf:type', 'Course'),
            Triple(item['code'], 'name', item['name']),
            Triple(item['code'], 'department',
                   uri(item['department']['code']))]
    elif isinstance(item, CourseOverviewItem):
        subject = item['course']['code']
        return [
            Triple(subject, 'extent', item['extent']),
            Triple(subject, 'teaching_period', item['teaching_period']),
            Triple(subject, 'learning_outcomes',
                   item['learning_outcomes']),
            Triple(subject, 'content', item['content']),
            Triple(subject, 'prerequisites', item['prerequisites']),
            Triple(subject, 'study_materials', item['study_materials'])]


class SIBPipeline(object):

    def __init__(self):
        self.sc = SIBConnection(method='preconfigured')
        self.sc.open()

    def __del__(self):
        self.sc.close()

    def process_item(self, spider, item):
        triples = [triple for triple in transform_to_triples(item)
                   if triple.object]
        self.sc.insert(triples)
        return item
