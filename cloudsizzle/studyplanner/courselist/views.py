"""Views for browsing through available courses"""
from django.shortcuts import render_to_response
from studyplanner.courselist.models import Course
from studyplanner.courselist.models import Faculty
from studyplanner.courselist.models import Department
from cloudsizzle import api

def list_faculties(request):
    faculties = api.course.get_faculties()
    return render_to_response('courselist/list_faculties.html', {'user': request.user,
        'faculties': faculties})

def list_departments(request, faculty):
    faculty = api.course.get_faculty_info(faculty)
    print "faculty:"
    print faculty
    departments = api.course.get_departments_by_faculty(faculty['code'])

    return render_to_response('courselist/list_departments.html', {'user': request.user,
        'faculty': faculty, 'departments': departments})

def list_courses(request, faculty, department):
    # Faculty information is neeed for breadcrumbs
    faculty = api.course.get_faculty_info(faculty)
    department = api.course.get_department_info(department)
    
    courses = api.course.get_courses_by_department(department['code'])

    return render_to_response('courselist/list_courses.html', {'user': request.user,
        'faculty': faculty, 'department': department, 'courses': courses})


def show_course(request, faculty, department, course):
    faculty = api.course.get_faculty_info(faculty)
    department = api.course.get_department_info(department)
    
    course = api.course.get_course(course)
    
    return render_to_response('courselist/show_course.html', {'user': request.user,
        'faculty': faculty, 'department': department, 'course': course})
