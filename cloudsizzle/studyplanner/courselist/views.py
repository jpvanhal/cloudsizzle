# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from cloudsizzle.courselist.models import Course

def index(request):
    course_list = Course.objects.all() 
    t = loader.get_template('UI1.0.html')
    c = Context({'courselist': course_list})
    return HttpResponse(t.render(c))
