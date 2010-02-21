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

"""Views for browsing through available courses."""

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from studyplanner.common.planner_session import check_authentication
from studyplanner.frontpage.models import PlannedCourse
from studyplanner.courselist import utils
from cloudsizzle.settings import ASI_BASE_URL
import api


@check_authentication
def list_faculties(request):
    faculties = api.course.get_faculties()
    return render_to_response('courselist/list_faculties.html',
        {
            'asi_session': request.session['asi_session'],
            'faculties': faculties
        },
        context_instance=RequestContext(request))


@check_authentication
def list_departments(request, faculty):
    try:
        # Faculty is needed for breadcrumbs
        faculty = api.course.get_faculty_info(faculty)
        departments = api.course.get_departments_by_faculty(faculty['code'])
    except Exception:
        raise Http404

    return render_to_response('courselist/list_departments.html',
        {
            'asi_session': request.session['asi_session'],
            'faculty': faculty,
            'departments': departments
        },
        context_instance=RequestContext(request))


@check_authentication
def list_courses(request, faculty, department):
    try:
        # Faculty & department information is needed for breadcrumbs
        faculty = api.course.get_faculty_info(faculty)
        department = api.course.get_department_info(department)
    except Exception:
        raise Http404
    courses = api.course.get_courses_by_department(department['code'])
    asi_session = request.session['asi_session']

    for course in courses:
        course['friendcount'] = utils.count_friends_taking_course(
                                    asi_session.user_id, course['code'])

    return render_to_response('courselist/list_courses.html',
        {
            'asi_session': asi_session,
            'faculty': faculty,
            'department': department,
            'courses': courses
        },
        context_instance=RequestContext(request))


@check_authentication
def show_course(request, faculty, department, course):
    try:
        # Faculty & department for breadcrumbs
        faculty = api.course.get_faculty_info(faculty)
        department = api.course.get_department_info(department)
        course = api.course.get_course(course)
    except Exception:
        raise Http404

    asi_session = request.session['asi_session']
    uid = asi_session.user_id

    isplanned = PlannedCourse.objects.filter(user_id=uid,
                                     course_code=course['code']).count() > 0

    iscompleted = asi_session.is_completed_course(course['code'])

    fids = utils.friends_taking_course(uid, course['code'])
    friends = []
    for fid in fids:
        try:
            friend = api.people.get(fid)
            friends.append(friend)
        except api.people.UserDoesNotExist:
            # Invalid friend relationship where friend does not exist in ASI
            pass

    print friends

    return render_to_response('courselist/show_course.html',
        {
            'ASI_BASE_URL': ASI_BASE_URL,
            'asi_session': request.session['asi_session'],
            'faculty': faculty,
            'department': department,
            'course': course,
            'isplanned': isplanned,
            'friends': friends,
            'iscompleted': iscompleted
        },
        context_instance=RequestContext(request))
