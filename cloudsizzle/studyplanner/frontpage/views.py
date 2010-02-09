from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
from common.forms import LoginForm, RegisterForm
from common.planner_session import is_authenticated, authenticate
from cloudsizzle.api.session import LoginFailed

def index(request):
    print "Index view requested"
    if is_authenticated(request):
        return home(request)
    else:
        return login_register(request)

def login_register(request):
    # Django standard form processing pattern:
    # User submitted form by POST
    if request.method == 'POST':
        print "login_register view posted"
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)

        if login_form.is_valid() and request.POST['submit'] == 'Login':
            # Use API to try to login
            # Write results to form if failed
            # Otherwise show home here
            print "login form was valid"
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                authenticate(request, username, password)
            except LoginFailed:
                # There is probably a smarter way for this, perhaps
                # a separate view?
                return HttpResponseRedirect('/?loginfailed')
            return HttpResponseRedirect('/')

        elif register_form.is_valid():
            # Use API to try and register
            # If fails write errors to form
            # Otherwise login and show home here
            print "register form was valid"
            return HttpResponseRedirect('/registered/')
    # User loaded page with form
    else:
        print "login-request view getted"
        login_form = LoginForm()
        register_form = RegisterForm()
        
    return render_to_response('frontpage/login-register.html',
        {'loginform': login_form, 'registerform': register_form,
    })
                
def logout(request):
    """Log the user out. Removes ASI connection from session"""
    # No reason to fail even if no session exists.
    if 'asi_session' in request.session:
#        request.session['asi_session'].close()
        del request.session['asi_session']
    
    return HttpResponseRedirect('/')
    
#for the mockups if anyone feels like it they should move this code to the
# appropriate file and application.

def home(request):
    print "Home requested"
    t = loader.get_template("frontpage/home.html")
    c = Context({ 'asi_session': request.session['asi_session'] })
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

def planned_courses(request):
    t = loader.get_template("frontpage/planned_courses.html")
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


