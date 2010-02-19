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

from django.conf.urls.defaults import url, patterns, include
from django.conf import settings

urlpatterns = patterns('',
    url(
        r'^$',
        'studyplanner.frontpage.views.index',
        name='frontpage'
    ),
    url(r'^login/?$', 'studyplanner.frontpage.views.login', name='login'),

    url(
        r'^session/logout/$',
        'studyplanner.frontpage.views.logout',
        name='logout_user'
    ),

    url(
        r'^home/$',
        'studyplanner.frontpage.views.home',
        name='home'
    ),

    url(
        r'^welcome/$',
        'studyplanner.frontpage.views.welcome',
        name='welcome'
    ),

    url(
        r'^profile/add_friend/(?P<user_id>[a-zA-Z0-9-_]+)/$',
        'studyplanner.frontpage.views.add_friend',
        name='addfriend'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/courses/completed/$',
        'studyplanner.frontpage.views.completed_courses',
        name='completed_courses'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/courses/friends/$',
        'studyplanner.frontpage.views.friends_courses',
        name='friendscourses'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/courses/planned/$',
        'studyplanner.frontpage.views.planned_courses',
        name='plannedcourses'
    ),

    url(
        r'^profile/courses/planned/add/$',
        'studyplanner.frontpage.views.add_to_planned_courses',
        name='add_to_planned_courses'
    ),

    url(
        r'^profile/courses/planned/remove/$',
        'studyplanner.frontpage.views.remove_planned_course',
        name='remove_from_planned_courses'
    ),

    url(
        r'^profile/$',
        'studyplanner.frontpage.views.profile',
        name='profile'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)$',
        'studyplanner.frontpage.views.profile',
        name='profile'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/friends/$',
        'studyplanner.frontpage.views.list_friends',
        name='friends'
    ),

    url(
        r'^registrations/$',
        'studyplanner.frontpage.views.registrations',
        name='registrations'
    ),

    url(
        r'^recommendcourse/(?P<coursecode>[a-zA-Z0-9-\.]+)$',
        'studyplanner.frontpage.views.recommendcourse',
        name='recommendcourse'
    ),

    url(
        r'^recommendtofriends/(?P<coursecode>[a-zA-Z0-9-\.]+)$',
        'studyplanner.frontpage.views.recommend_to_friends',
        name='recommendtofriends'
    ),

    url(
        r'^search/$',
        'studyplanner.frontpage.views.search',
        name='search'
    ),

    url(
        r'^internalerror/$',
        'studyplanner.frontpage.views.internal_error',
        name='internalerror'
    ),

    url(r'^courses/', include('courselist.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
    ))
