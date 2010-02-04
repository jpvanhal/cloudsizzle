# Create your views here.
from django.shortcuts import render_to_response
from studyplanner.courselist.models import Course
from studyplanner.courselist.models import Faculty
from studyplanner.courselist.models import Department
from cloudsizzle.api.course import get_faculties, get_departments_by_faculty, get_courses_by_department, get_course

def list_courses(request, faculty, department):
    courses = get_courses_by_department(department)
    department = {'slug': str(department)}
    return render_to_response('courselist/list_courses.html', {'user': request.user,
        'department': department, 'courses': courses})

def list_faculties(request):
#    faculties = Faculty.objects.all()
    faculties = get_faculties()
    print faculties
    return render_to_response('courselist/list_faculties.html', {'user': request.user,
        'faculties': faculties})

def list_departments(request, faculty):
#    faculty = Faculty.objects.get(slug=faculty)
#    departments = faculty.departments.all()

    departments = get_departments_by_faculty(faculty)
    faculty = {'slug': str(faculty)}
    return render_to_response('courselist/list_departments.html', {'user': request.user,
        'faculty': faculty, 'departments': departments})

def show_course(request, faculty, department, course):
#    faculty = Faculty.objects.get(slug=faculty)
#    department = Department.objects.get(slug=department)
#    course = Course.objects.get(slug=course)
    course = get_course(course)
    return render_to_response('courselist/show_course.html', {'user': request.user,
        'faculty': faculty, 'department': department, 'course': course})
