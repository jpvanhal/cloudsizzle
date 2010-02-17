"""Views for browsing through available courses"""
from django.template import RequestContext
from django.shortcuts import render_to_response
from studyplanner.common.planner_session import check_authentication
from studyplanner.courselist.models import Course
from studyplanner.courselist.models import Faculty
from studyplanner.courselist.models import Department
from studyplanner.frontpage.models import PlannedCourse
from studyplanner.courselist import utils
import api

@check_authentication
def list_faculties(request):
    faculties = api.course.get_faculties()
    return render_to_response('courselist/list_faculties.html',
        {'asi_session': request.session['asi_session'],
        'faculties': faculties},
        context_instance=RequestContext(request))

@check_authentication
def list_departments(request, faculty):
    faculty = api.course.get_faculty_info(faculty)
    departments = api.course.get_departments_by_faculty(faculty['code'])

    return render_to_response('courselist/list_departments.html',
        {'asi_session': request.session['asi_session'],
        'faculty': faculty, 'departments': departments},
        context_instance=RequestContext(request))

@check_authentication
def list_courses(request, faculty, department):
    # Faculty information is neeed for breadcrumbs
    faculty = api.course.get_faculty_info(faculty)
    department = api.course.get_department_info(department)
    courses = api.course.get_courses_by_department(department['code'])
    asi_session = request.session['asi_session']
    
    for course in courses:
        course['friendcount'] = utils.count_friends_taking_course(
                                    asi_session.user_id, course['code'])
                                
    return render_to_response('courselist/list_courses.html',
        {'asi_session': asi_session,
        'faculty': faculty, 'department': department, 'courses': courses},
        context_instance=RequestContext(request))

@check_authentication
def show_course(request, faculty, department, course):
    faculty = api.course.get_faculty_info(faculty)
    department = api.course.get_department_info(department)
    
    course = api.course.get_course(course)
    
    #check if user has planned to take the course
    asi_session = request.session['asi_session']
    uid = asi_session.user_id

    # Standard database stuff, check for existence by counting
    # This should be made a function and moved to utils
    isplanned = PlannedCourse.objects.filter(user_id=uid,
                                     course_code=course['code']).count() > 0
    
    iscompleted = asi_session.is_completed_course(course['code'])
                                     
    fids = utils.friends_taking_course(uid, course['code'])
    friends = []
    for fid in fids:
        friend = api.people.get(fid)
        friend['user_id'] = fid
        friends.append(friend)
    
    print friends
    
    return render_to_response('courselist/show_course.html',
        {'asi_session': request.session['asi_session'],
        'faculty': faculty, 'department': department, 'course': course,
        'isplanned': isplanned, 'friends': friends, 'iscompleted': iscompleted},
        context_instance=RequestContext(request))
