# Create your views here.
from django.shortcuts import render_to_response
from studyplanner.courselist.models import Course
from studyplanner.courselist.models import Faculty
from studyplanner.courselist.models import Department

def list_courses(request, faculty, department):
    department = Department.objects.get(slug=department)
    courses = department.courses.all()
    return render_to_response('list_courses.html', {
        'department': department, 'courses': courses})

def list_faculties(request):
    faculties = Faculty.objects.all()
    return render_to_response('list_faculties.html', {'faculties': faculties})

def list_departments(request, faculty):
    faculty = Faculty.objects.get(slug=faculty)
    departments = faculty.departments.all()
    return render_to_response('list_departments.html', {
        'faculty': faculty, 'departments': departments})

def show_course(request, faculty, department, course):
    faculty = Faculty.objects.get(slug=faculty)
    department = Department.objects.get(slug=department)
    course = Course.objects.get(slug=course)
    return render_to_response('show_course.html', {
        'faculty': faculty, 'department': department, 'course': course})
