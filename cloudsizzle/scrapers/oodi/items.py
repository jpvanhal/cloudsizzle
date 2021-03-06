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
The models for scraped items.

See documentation in:

http://doc.scrapy.org/topics/items.html

"""
from scrapy.item import Item, Field
from cloudsizzle.scrapers.items import DateField


class CompletedCourseItem(Item):
    name = Field()
    code = Field()
    cr = Field()
    ocr = Field()
    grade = Field()
    date = DateField('%d.%m.%Y')
    teacher = Field()
    module = Field()


class ModuleItem(Item):
    name = Field()
    code = Field()
