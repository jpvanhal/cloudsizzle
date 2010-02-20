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

"""Utility functions related to courses."""

from studyplanner.frontpage.models import PlannedCourse
import api


def courses_taken_by_friends(user_id):
    """Get courses that a friends of user are taking. Also provides
    friendcount for the courses.

    Arguments:
    user_id --- ASI user ID for the person the friends will
                be searched through. Case sensitive

    Return value:
    [{'code': u'Mat-1.1131',
     'content': 'Kompleksianalyysi. z-muunnos. Fourier-analyysi.',
     'department': 'T3020',
     'extent': '5',
     'faculty': 'il',
     'friendcount': 1,
     'learning_outcomes': 'Antaa tutkinto-ohjelmassa tarvittavat perustiedot '
        'kurssin aihepiiristä. Vahvistaa opiskelijan matemaattista '
        'ajattelutapaa. Harjaannuttaa käytännön ongelmien matemaattiseen '
        'muotoiluun. Perehdyttää kurssilla esitettävien menetelmien '
        'soveltamiseen.',
     'name': 'Matematiikan peruskurssi C3-I',
     'prerequisites': 'Matematiikan peruskurssit L/C 1-2',
     'study_materials': 'Kreyszig: Advanced Engineering Mathematics, 9.painos.',
     'teaching_period': 'I'}]

    """
    from django.db import connection

    friends = api.people.get_friends(user_id)
    # Django ORM cannot handle this because we use single table
    #coursecodes = PlannedCourse.objects.filter(user_id__in=friends) \
    #                           .annotate(Count('user_id')) \
    #                           .values_list('course_code','user_id__count')

    # So let's use raw SQL
    cursor = connection.cursor()

    # It seems I have to build this string by myself
    # This also means that corrupt data in smart-m3 can perform SQL injection
    whereclause = ""
    for friend in friends:
        whereclause += ("'{0}',".format(friend))
    whereclause = whereclause[:-1]

    query = """
        SELECT course_code, COUNT(course_code)
        FROM frontpage_plannedcourse
        WHERE user_id IN ({0})
        GROUP BY course_code""".format(whereclause)
    cursor.execute(query)
    coursecodes = cursor.fetchall()
    #OK. That was insane. Not to mention PHPish.

    courses = []
    for (code, count) in coursecodes:
        coursedata = api.course.get_course(code)
        coursedata['friendcount'] = count
        courses.append(coursedata)

    return courses


def friends_taking_course(user_id, course_code):
    """Get friends taking a specific course

    Arguments:
    user_id --- ASI user ID for the person whose friends will
                be searched through. Case sensitive
    course_code -- Course code for the course being counted.
                   Case sensitive

    """
    friends = api.people.get_friends(user_id)

    friends_on_course = PlannedCourse.objects \
        .filter(user_id__in=friends, course_code=course_code) \
        .values_list('user_id', flat=True)

    return friends_on_course


def count_friends_taking_course(user_id, course_code):
    """Count friends taking a specific course

    Arguments:
    user_id --- ASI user ID for the person whose friends will
                be searched through. Case sensitive
    course_code -- Course code for the course being counted.
                   Case sensitive

    """
    friends = api.people.get_friends(user_id)

    count_of_friends = PlannedCourse.objects \
        .filter(user_id__in=friends, course_code=course_code) \
        .count()

    return count_of_friends

def mutual_courses(user_id1, user_id2):
    """Get list of mutual courses between two users
    
    Arguments:
    user_id1, user_id2 --- ASI users between whom the common courses
                           should be searched
    
    """
    from django.db import connection
    
    query = """
        SELECT a1.course_code
        FROM frontpage_plannedcourse as a1, frontpage_plannedcourse as a2
        WHERE a1.user_id = %s AND
              a2.user_id = %s AND
              a1.course_code = a2.course_code"""
    
    cursor = connection.cursor()
    cursor.execute(query, [user_id1, user_id2])
    
    course_select = cursor.fetchall()
    
    courses = [code[0] for code in course_select]
    
    return courses
