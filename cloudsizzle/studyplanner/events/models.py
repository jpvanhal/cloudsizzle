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

from django.db import models


class Event(models.Model):
    user_id = models.CharField(max_length=22)
    time = models.DateTimeField(auto_now_add=True)


class PlannedCourse(Event):
    course_code = models.CharField(max_length=30)


class FriendRequest(Event):
    new_friend = models.CharField(max_length=22)


class NewFriendEvent(Event):
    new_friend = models.CharField(max_length=22)


class EventsLog(Event):
    '''
    #this action can be "'became a friend of'" for friend adding or
    'enrolled to' for planing course. object should be friend_id or
    department_code#course_code
    '''
    action = models.CharField(max_length=40)
    object = models.CharField(max_length=30)
