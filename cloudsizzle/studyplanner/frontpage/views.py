from django.http import HttpResponse
from django.template import Context, loader
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def index(request):
    t = loader.get_template("frontpage/login-register.html")
    c = Context({'loginform': AuthenticationForm(),
                 'registerform': RegisterForm()})
    return HttpResponse(t.render(c))


class RegisterForm(UserCreationForm):
    firstname = forms.CharField(label='First name', widget=forms.TextInput())
    lastname = forms.CharField(label='Last name', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.TextInput())

#for the mockups if anyone feels like it they should move this code to the
# appropriate file and application.

def home(request):
    t = loader.get_template("frontpage/home.html")
    c = Context({})
    return HttpResponse(t.render(c))

def profile(request):
    t = loader.get_template("frontpage/profile.html")
    c = Context({})
    return HttpResponse(t.render(c))

def friends(request):
    t = loader.get_template("frontpage/friends.html")
    c = Context({})
    return HttpResponse(t.render(c))

def registrations(request):
    t = loader.get_template("frontpage/registrations.html")
    c = Context({})
    return HttpResponse(t.render(c))

def completedstudies(request):
    t = loader.get_template("frontpage/completed_studies.html")
    c = Context({})
    return HttpResponse(t.render(c))

def friendscourses(request):
    t = loader.get_template("frontpage/friends_courses.html")
    c = Context({})
    return HttpResponse(t.render(c))

def courses(request):
    t = loader.get_template("frontpage/courses.html")
    c = Context({})
    return HttpResponse(t.render(c))

def coursesfaculty(request):
    t = loader.get_template("frontpage/courses_faculty.html")
    c = Context({})
    return HttpResponse(t.render(c))

def coursesdepartment(request):
    t = loader.get_template("frontpage/courses_department.html")
    c = Context({})
    return HttpResponse(t.render(c))

def course(request):
    t = loader.get_template("frontpage/course.html")
    c = Context({})
    return HttpResponse(t.render(c))

def recommendedcourse(request):
    t = loader.get_template("frontpage/recommend_course.html")
    c = Context({})
    return HttpResponse(t.render(c))

def generalinfo(request):
    t = loader.get_template("frontpage/general_info.html")
    c = Context({})
    return HttpResponse(t.render(c))

def privacy(request):
    t = loader.get_template("frontpage/privacy.html")
    c = Context({})
    return HttpResponse(t.render(c))

def search(request):
    t = loader.get_template("frontpage/search.html")
    c = Context({})
    return HttpResponse(t.render(c))

def notifications(request):
    t = loader.get_template("frontpage/notifications.html")
    c = Context({})
    return HttpResponse(t.render(c))


