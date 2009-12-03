from django.http import HttpResponse
from django.template import Context, loader
from studyplanner.courselist.views import courselist
from studyplanner.courselist.views import facultylist
from studyplanner.courselist.views import departmentlist


def courselist(request):
    t = loader.get_template('UI1.0.html')
    c = Context({'list':  courselist(request).content })
    return HttpResponse(t.render(c))


def facultylist(request):
    t = loader.get_template('UI1.0.html')
    c = Context({'list':  facultylist(request).content })
    return HttpResponse(t.render(c))
    
def departmentlist(request):
    t = loader.get_template('UI1.0.html')
    c = Context({'list':  departmentlist(request).content })
    return HttpResponse(t.render(c))


