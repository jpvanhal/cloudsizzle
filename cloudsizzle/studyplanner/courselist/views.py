"""Views for browsing through available courses"""
from django.shortcuts import render_to_response
from studyplanner.common.planner_session import check_authentication
from studyplanner.courselist.models import Course
from studyplanner.courselist.models import Faculty
from studyplanner.courselist.models import Department
import api

@check_authentication
def list_faculties(request):
    faculties = api.course.get_faculties()
    print request.session['asi_session'].user_id
    return render_to_response('courselist/list_faculties.html',
        {'asi_session': request.session['asi_session'],
        'faculties': faculties})

@check_authentication
def list_departments(request, faculty):
    faculty = api.course.get_faculty_info(faculty)
    departments = api.course.get_departments_by_faculty(faculty['code'])

    return render_to_response('courselist/list_departments.html',
        {'asi_session': request.session['asi_session'],
        'faculty': faculty, 'departments': departments})

@check_authentication
def list_courses(request, faculty, department):
    # Faculty information is neeed for breadcrumbs
    faculty = api.course.get_faculty_info(faculty)
    department = api.course.get_department_info(department)
    courses = api.course.get_courses_by_department(department['code'])

    return render_to_response('courselist/list_courses.html',
        {'asi_session': request.session['asi_session'],
        'faculty': faculty, 'department': department, 'courses': courses})

@check_authentication
def show_course(request, faculty, department, course):
    faculty = api.course.get_faculty_info(faculty)
    department = api.course.get_department_info(department)
    
    course = api.course.get_course(course)
    
    return render_to_response('courselist/show_course.html',
        {'asi_session': request.session['asi_session'],
        'faculty': faculty, 'department': department, 'course': course})

def show_bare_course(request, course):
    course = api.course.get_course(course)
    
    return render_to_response('courselist/show_course.html',
        {'asi_session': request.session['asi_session'],
        'course': course})
