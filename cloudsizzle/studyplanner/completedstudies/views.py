# Create your views here.
from studyplanner.completedstudies.models import CompletedCourse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    courses = CompletedCourse.objects.filter(student=request.user)
    return render_to_response('completed.html', {'user': request.user,
        'courses': courses})
