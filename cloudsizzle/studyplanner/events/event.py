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

'''
Created on Feb 14, 2010

@author: pb
'''

from django.core.urlresolvers import reverse
from cloudsizzle.studyplanner.events.models import Event
from cloudsizzle import api
from cloudsizzle.settings import ASI_BASE_URL
from cloudsizzle.studyplanner.frontpage.models import RecommendedCourse

class EventLog:

    def __init__(self, img_scr='', user_name='', user_scr='', action='',
                       object_name='', object_scr='', update_time=''):
        self.img_scr = img_scr
        self.user_name = user_name
        self.user_scr = user_scr
        self.action = action
        self.object_name = object_name
        self.object_scr = object_scr
        self.update_time = update_time

    @classmethod
    def get_notifications(cls, user_id):
        if user_id == None:
            return []
        result = []
        notifications = RecommendedCourse.get_all_recommended_courses(user_id)
        for notification in notifications:
            user_id = notification.user_recommending
            img_scr = ASI_BASE_URL + '/people/' + user_id \
                    + '/@avatar/small_thumbnail'
            user_scr = reverse('profile', args=[user_id])
            try:
                user_inf = api.people.get(user_id)
            except api.people.UserDoesNotExist:
                continue
            try:
                user_name = user_inf['username']
            except (KeyError, TypeError):
                user_name = 'Unknown'
            course_code = notification.course_code
            object_name = course_code
            action = 'recommends'
            update_time = notification.time
            result.append(PlanCourseEventLog(img_scr=img_scr,
                user_name=user_name, user_scr=user_scr, action=action,
                object_name=object_name, update_time=update_time,
                object_id=course_code))
        return result

    @classmethod
    def constructor(cls, user_ids):
        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        if user_ids == []:
            return []
        events = Event.objects.filter(user_id__in=user_ids) \
                              .order_by('-time')[0:10]
        if len(user_ids) == 1:    # only one id input use builder once.
            return cls.builder(user_id=user_ids[0], events=events)
        else:                     # many ids input give every id a builder.
            result = []
            for event in events:
                result.extend(cls.builder(event.user_id, events=[event]))
            return result

    @classmethod
    def builder(cls, user_id, events):
        feeds = []
        img_scr = ASI_BASE_URL + '/people/' + user_id \
                + '/@avatar/small_thumbnail'
        user_scr = reverse('profile', args=[user_id])

        try:
            user_inf = api.people.get(user_id)
        except api.people.UserDoesNotExist:
            return []

        try:
            user_name = user_inf['username']
        except (KeyError, TypeError):
            user_name = 'Unknown'

        if not events:
            return []

        for event in events:
            update_time = event.time
            # plan course event get course name, and department and faculty code
            if hasattr(event, 'plannedcourse'):
                course_code = event.plannedcourse.course_code
                object_name = course_code
                action = 'plans to take'
                feeds.append(PlanCourseEventLog(img_scr=img_scr,
                    user_name=user_name, user_scr=user_scr, action=action,
                    object_name=object_name, update_time=update_time,
                    object_id=course_code))
            #  new friends event get friend's url and name.
            if hasattr(event, 'newfriendevent'):
                friend_id = event.newfriendevent.new_friend
                try:
                    friend_inf = api.people.get(friend_id)
                except api.people.UserDoesNotExist:
                    continue
                try:
                    friend_name = friend_inf['username']
                except (KeyError, TypeError):
                    friend_name = 'Unknown'
                object_name = friend_name
                action = 'became friend with'
                feeds.append(NewFriendEventLog(img_scr=img_scr,
                    user_name=user_name, user_scr=user_scr, action=action,
                    object_name=object_name, update_time=update_time,
                    object_id=friend_id))
        return feeds

    def _get_object_scr(self, object_name):
        return ''


class PlanCourseEventLog(EventLog):

    def __init__(self, img_scr='', user_name='', user_scr='', action='',
                       object_name='', update_time='', object_id=''):
        self.course_name = object_name + ' '
        object_scr = self._get_object_scr(object_id)
        EventLog.__init__(self, img_scr=img_scr, user_name=user_name,
            user_scr=user_scr, action=action, object_name=self.course_name,
            object_scr=object_scr, update_time=update_time)

    def _get_object_scr(self, object_id):
        courseinfo = api.course.get_course(object_id)
        self.course_name += courseinfo['name']
        return reverse('show_course', args=[
            courseinfo['faculty'],
            courseinfo['department'],
            courseinfo['code']])


class NewFriendEventLog(EventLog):

    def __init__(self, img_scr='', user_name='', user_scr='', action='',
                       object_name='', update_time='', object_id=''):
        object_scr = self._get_object_scr(object_id)
        EventLog.__init__(self, img_scr=img_scr, user_name=user_name,
            user_scr=user_scr, action=action, object_name=object_name,
            object_scr=object_scr, update_time=update_time)

    def _get_object_scr(self, object_id):
        return reverse('profile', args=[object_id])
