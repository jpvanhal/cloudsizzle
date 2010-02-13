from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
from django import forms
from studyplanner.common.forms import LoginForm, RegisterForm
from studyplanner.common.planner_session import is_authenticated, authenticate
from studyplanner.common.planner_session import check_authentication
import api
from studyplanner.events.models import Event
from cloudsizzle.asi.client import TimeOutError

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
                print 'calling authenticate'
                authenticate(request, username, password)
                print 'authenticate returned'
            except api.LoginFailed as message:
                # There is probably a smarter way for this, perhaps
                # a separate view?
                print "LoginFailed message:-----------"
                print type(message)
                print message
                return HttpResponseRedirect('/?loginfailed')
            except TimeOutError:
                print "Timeout while authenticating"
                return HttpResponseRedirect('internalerror')
            return HttpResponseRedirect('/')

        elif register_form.is_valid():
            # Use API to try and register
            # If fails write errors to form
            # Otherwise login and show home here
            print "register form was valid"
            username = register_form.cleaned_data['username']
            firstname = register_form.cleaned_data['firstname']
            lastname = register_form.cleaned_data['lastname']
            password = register_form.cleaned_data['password']
            # Django has verified password
            email = register_form.cleaned_data['email']
            # Django has verified that consent is checked
            
            print "Calling api people.create"
            api.people.create(username, password, email)

            print "Calling authenticate after register"
            try:
                authenticate(request, username, password)
            except api.LoginFailed:
                # This means that the user who was succesfully
                # registered could not authenticate.
                print "Successful register -> failed auth"
                return HttpResponseRedirect('/internalerror')
            except TimeOutError:
                print "Timeout while authenticating"
                return HttpResponseRedirect('/internalerror')
            return HttpResponseRedirect('/welcome/')
    # User loaded page with form
    else:
        print "login-request view getted"
        login_form = LoginForm()
        register_form = RegisterForm()

    return render_to_response('frontpage/login-register.html',
        {'loginform': login_form, 'registerform': register_form,
    })

def welcome(request):
    return render_to_response('frontpage/welcome.html',
        {'asi_session': request.session['asi_session'],
    })
                
def logout(request):
    """Log the user out. Removes ASI connection from session"""
    # No reason to fail even if no session exists.
    if 'asi_session' in request.session:
        print 'Closing session'
        request.session['asi_session'].close()
        print 'Session closed'
        del request.session['asi_session']
    
    return HttpResponseRedirect('/')
    
#for the mockups if anyone feels like it they should move this code to the
# appropriate file and application.

def home(request):
#    events = request.session['asi_session'].get_events()
    t = loader.get_template("frontpage/home.html")
    c = Context({ 'asi_session': request.session['asi_session'],
                  #'events': events
                  })
    return HttpResponse(t.render(c))

def profile(request, user_id):
    profile_user = api.people.get(user_id)
    profile_user['user_id'] = user_id

    t = loader.get_template("frontpage/profile.html")
    try:
        session = request.session['asi_session']
    except KeyError:
        return HttpResponseRedirect('/home/')
    username = session.username
    user_id = session.user_id
    user_inf = api.people.get(user_id)
    try:
        real_name = user_inf['name']
        sex = user_inf['gender']
        email = user_inf['email']
    except KeyError:
        real_name = sex = email =""
    #user_pic = session.getpic()
    c = Context({'username':username, 'real_name':real_name, 'sex':sex, 'email':email, 'asi_session': session, 'profile_user': profile_user})
    return HttpResponse(t.render(c))

def friends(request, user_id):
    asi_session = request.session['asi_session']

    profile_user = api.people.get(user_id)
    profile_user['user_id'] = user_id

    friend_ids = api.people.get_friends(user_id)
    friends = []
    
    for friend_id in friend_ids:
        friend = api.people.get(friend_id)
        friend['user_id'] = friend_id
        
        friends.append(friend)
    
    pending_friend_ids = asi_session.get_pending_friend_requests()
    pending_requests = []
    
    for id in pending_friend_ids:
        pending = api.people.get(id)
        pending['user_id'] = id
        
        pending_requests.append(pending)
    
    t = loader.get_template("frontpage/friends.html")
    c = Context({'asi_session': request.session['asi_session'],
                 'friends': friends, 'requests': pending_requests,
                 'profile_user': profile_user})
    return HttpResponse(t.render(c))

def add_friend(request, user_id):
    print "add_friend called"
    session = request.session['asi_session']
    own_id = session.user_id
    print "adding friend: " + user_id
    session.add_friend(user_id)
    print "add returned"
    
    return HttpResponseRedirect(reverse("friends", args=[own_id]))

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

class SearchForm(forms.Form):
    # Required fields have * at the end of label
    query = forms.CharField(min_length=4, max_length=40, label="Keywords")
    scope = forms.ChoiceField([('all', 'All content'), ('courses', 'Courses'), ('users', 'Users')], label="Search option")

@check_authentication
def search(request):
    t = loader.get_template("frontpage/search.html")
    searchform = SearchForm(request.GET)
    if searchform.is_valid():
        query = searchform.cleaned_data['query']
        scope = searchform.cleaned_data['scope']
        results = []
        
        if scope == 'all' or scope == 'users':
            for userid in api.people.search(query):
                details = api.people.get(userid)
                results.append(
                    {'type':'user', 'userid':userid,
                    'username':details['username'],}
                )
        if scope == 'all' or scope == 'courses':
            for coursecode in api.course.search(query):
                details = api.course.get_course(coursecode)
                results.append(
                    {'type':'course', 'code': coursecode,
                    'name':details['name']}
                )
        
        
        c = Context({'searchform': searchform, 'results': results,
                     'query': query,
                     'asi_session': request.session['asi_session']
            })
    else:
        c = Context({'searchform': searchform})
    return HttpResponse(t.render(c))

def notifications(request):
    t = loader.get_template("frontpage/notifications.html")
    c = Context({})
    return HttpResponse(t.render(c))
