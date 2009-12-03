# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from studyplanner.courselist.models import Course
from studyplanner.courselist.models import Faculty
from studyplanner.courselist.models import Department

def courselist(request):
    course_list = Course.objects.all() 
    t = loader.get_template('list.html')
    c = Context({'list': course_list})
    return HttpResponse(t.render(c))
    
    
def facultylist(request):
    faculty_list = Faculty.objects.all() 
    t = loader.get_template('list.html')
    c = Context({'list': faculty_list})
    return HttpResponse(t.render(c))
    

def departmentlist(request):
    department_list = Department.objects.all() 
    t = loader.get_template('list.html')
    c = Context({'list': department_list})
    return HttpResponse(t.render(c))
    
