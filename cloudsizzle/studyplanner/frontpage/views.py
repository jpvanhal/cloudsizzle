"""Frontpage view that handles most of the study planner. Probably needs to be
split into individual applications or files.

"""
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django import forms
from studyplanner.common.forms import LoginForm, RegisterForm
from studyplanner.common.planner_session import is_authenticated, authenticate
from studyplanner.common.planner_session import check_authentication
from studyplanner.events.event import EventLog
import api
from studyplanner.events.models import Event, PlannedCourse as PlannedCourseEvent
from studyplanner.frontpage.models import PlannedCourse
from cloudsizzle.asi.client import TimeOutError
from studyplanner.courselist import utils
from cloudsizzle.settings import ASI_BASE_URL

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
                # Some way of passing the login failed message
                # to user is needed. Maybe it could be done inside
                # Django form handling?
                return HttpResponseRedirect(reverse('frontpage'))
            except TimeOutError:
                print "Timeout while authenticating"
                return HttpResponseRedirect(reverse('internalerror'))
            return HttpResponseRedirect(reverse('home'))

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
                return HttpResponseRedirect(reverse('internalerror'))
            except TimeOutError:
                print "Timeout while authenticating"
                return HttpResponseRedirect(reverse('internalerror'))
            return HttpResponseRedirect(reverse(welcome))
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

    return HttpResponseRedirect(reverse('frontpage'))

#for the mockups if anyone feels like it they should move this code to the
# appropriate file and application.

def home(request):
    asi_session = request.session['asi_session']
    user_id = asi_session.user_id
    friends = api.people.get_friends(user_id)        
    t = loader.get_template("frontpage/home.html")
    feedurl = 'frontpage/feeds.html'
    feeds = EventLog.constructor(user_ids=friends)
    c = Context({
    'asi_session': request.session['asi_session'],
        'feedurl':feedurl,
        'feeds':feeds,
    })
    return HttpResponse(t.render(c))
'''
discarded
def feed(request, user_id):
    t = loader.get_template("frontpage/feeds.html")
    # example
    feeds = [EventLog(img_scr='http://cos.alpha.sizl.org/people/bHC0t6gwur37J8aaWPEYjL/@avatar', user_name='pb', action="study", object_name='mew', object_scr='http://dict.cn/', update_time='2 hours'),\
             EventLog(img_scr='http://cos.alpha.sizl.org/people/bHC0t6gwur37J8aaWPEYjL/@avatar', user_name='pb', action="study", object_name='mew', object_scr='http://dict.cn/', update_time='2 hours'),]
    # All profile sub-pages need to have the template name in Context, this is
    # used to correctly render the active tab in the common parent template
    c = Context({'feeds':feeds, 'template':profile})
    return HttpResponse(t.render(c))
'''

@check_authentication
def profile(request, user_id=None):
    t = loader.get_template("frontpage/profile.html")

    asi_session = request.session['asi_session']
    user_id = user_id if user_id else asi_session.user_id

    try:
        user = api.people.get(user_id)
    except api.people.UserDoesNotExist:
        raise Http404

    username = user['username']
    try:
        realname = user['name']['unstructured']
    except (KeyError, TypeError):
        realname = username
    try:
        avatar_url = '{0}{1}/large_thumbnail'.format(ASI_BASE_URL, user['avatar']['link']['href'])
    except (KeyError, TypeError):
        avatar_url = ''
    feedurl = 'frontpage/feeds.html'
    feeds = EventLog.constructor(user_ids=user_id)
    #feeds = EventLog.constructor(user_ids=['cwc2e4f14r362vaaWPEYjL','bHC0t6gwur37J8aaWPEYjL'])
    c = Context({
	'asi_session': request.session['asi_session'],
        'profile_user': user,
        'username': username,
        'realname': realname,
        'avatar_url': avatar_url,
        'template':'profile',
        'feedurl':feedurl,
        'feeds':feeds,
    })
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
                 'profile_user': profile_user, 'template': 'friends'})
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

@check_authentication
def completed_courses(request, user_id):
    t = loader.get_template("frontpage/profile_courses_completed.html")

    asi_session = request.session['asi_session']
    profile_user = api.people.get(asi_session.user_id)
    courses = asi_session.get_completed_courses()

    c = Context({
        'asi_session': asi_session,
        'profile_user': profile_user,
        'courses': courses,
        'template': 'profile_courses_completed',
    })

    return HttpResponse(t.render(c))

@check_authentication
def friends_courses(request, user_id):
    asi_session = request.session['asi_session']
    profile_user = api.people.get(asi_session.user_id)
    courses = utils.courses_taken_by_friends(user_id)

    return render_to_response(
        'frontpage/profile_courses_friends.html',
        {
            'profile_user': profile_user,
            'courses': courses, 
            'asi_session': asi_session,
            'template': 'profile_courses_friends'
    })

@check_authentication
def planned_courses(request, user_id):
    """
    If the request is GET this function returns
    a list of all planned courses.

    If the request is POST this function will
    add a course to the planned courses.
    """
    try:
        user = api.people.get(user_id)
    except api.people.UserDoesNotExist:
        raise Http404
        
    coursedb = PlannedCourse.objects.filter(user_id=user_id)
    planned_courses = []

    for course_entry in coursedb:
        course_code = course_entry.course_code
        planned_courses.append(api.course.get_course(course_code))

    t = loader.get_template("frontpage/profile_courses_planned.html")
    c = Context({
        'asi_session': request.session['asi_session'],
        'profile_user': user,
        'planned_courses': planned_courses,
        'template': 'profile_courses_planned',
    })
    return HttpResponse(t.render(c))

def add_to_planned_courses(request):
    if request.method == "POST":
        cc = request.POST.get('course_code', None)
        asi_session = request.session['asi_session']
        uid = asi_session.user_id

        if(cc != None):
            course = PlannedCourse(course_code=cc, user_id=uid)
            course.save()
            e = PlannedCourseEvent(course_code=cc, user_id=uid)
            e.save()
            request.method = "GET"
            return HttpResponseRedirect(reverse("plannedcourses", args=[uid]))
        else:
            return HttpResponseBadRequest("could not add course to planned courses")

def remove_planned_course(request):
    """
    this method removes a course from planned courses
    we use this method because the AJAX http DELETE does not work
    with all browsers
    """
    cc = request.POST.get('course_code',None)
    asi_session = request.session['asi_session']
    uid = asi_session.user_id
    PlannedCourse.objects.filter(user_id = uid).filter(course_code = cc).delete()
    return HttpResponseRedirect(reverse("plannedcourses", args=[uid]))

def recommendcourse(request, coursecode):
    asi_session = request.session['asi_session']

    friend_ids = api.people.get_friends(asi_session.user_id)
    friends = []

    for friend_id in friend_ids:
        friend = api.people.get(friend_id)
        friend['user_id'] = friend_id

        friends.append(friend)

    course = api.course.get_course(coursecode)

    t = loader.get_template("frontpage/recommend_course.html")
    c = Context({'asi_session': asi_session,
                'friends': friends,
                'course': course})
    return HttpResponse(t.render(c))

def recommend_to_friends(request, coursecode):
    """
    This method takes a post form with friend id's and
    adds to their recommended courses.
    """
    res = request.POST
    print res

    return HttpResponseRedirect(reverse("home"))

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
        userresults = []
        courseresults = []

        if scope == 'all' or scope == 'users':
            for userid in api.people.search(query):
                details = api.people.get(userid)
                details['userid'] = userid
                userresults.append(details)
        if scope == 'all' or scope == 'courses':
            for coursecode in api.course.search(query):
                details = api.course.get_course(coursecode)
                courseresults.append(details)

        c = Context({'searchform': searchform, 'userresults': userresults,
                     'courseresults': courseresults, 'query': query,
                     'asi_session': request.session['asi_session']
            })
    else:
        c = Context({'searchform': searchform,
                    'asi_session': request.session['asi_session']})
    return HttpResponse(t.render(c))

def notifications(request):
    t = loader.get_template("frontpage/notifications.html")
    c = Context({})
    return HttpResponse(t.render(c))

def internal_error(request):
    return render_to_response('frontpage/internal_error.html')
