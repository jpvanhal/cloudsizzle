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

"""Django models related to the large frontpage-application."""
from django.db import models


class User(models.Model):
    """Base model for all information related to single user"""
    user_id = models.CharField(max_length=22, primary_key=True)
    # Neither of these used because of time constraints
    majorcode = models.CharField(max_length=15)
    minorcode = models.CharField(max_length=15)

    def __unicode__(self):
        return self.user_id


class PlannedCourse(models.Model):
    """Model containing users planned courses"""
    # Only course code is needed here, all other information is available
    # through API(tm)
    user_id = models.CharField(max_length=22)
    course_code = models.CharField(max_length=20)

    def __unicode__(self):
        return self.course_code + "/" + self.user_id
        
class RecommendedCourse(models.Model):
    """
    This is the model where we keep the courses
    that has been recommended.
    """
    user_recommending = models.CharField(max_length=22)
    user_recommended = models.CharField(max_length=22)
    course_code = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
