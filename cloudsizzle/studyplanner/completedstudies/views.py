# Create your views here.
from studyplanner.completedstudies.models import CompletedCourse
from django.shortcuts import render_to_response

def index(request):
    courses = CompletedCourse.objects.all()
    return render_to_response('completed.html', {
        'courses': courses})
