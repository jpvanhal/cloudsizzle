"""Frontpage view that handles most of the study planner. Probably needs to be
split into individual applications or files.

"""
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, Http404
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django import forms
from studyplanner.common.forms import LoginForm, RegisterForm
from studyplanner.common.planner_session import is_authenticated, authenticate
from studyplanner.common.planner_session import check_authentication
from studyplanner.events.event import EventLog
import api
from studyplanner.events.models import PlannedCourse as PlannedCourseEvent
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
                # assume that this always means bad username/password
                return HttpResponseRedirect(reverse('login'))
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

    return render_to_response(
        'frontpage/login-register.html',
        {
            'loginform': login_form,
            'registerform': register_form
        },
        context_instance=RequestContext(request))

"""Login page, only shown when wrong username or pssword is given"""
def login(request):
    login_form = LoginForm()

    return render_to_response('frontpage/login.html',
        {'loginform': login_form}
    )

def welcome(request):
    return render_to_response(
        'frontpage/welcome.html',
        {
            'asi_session': request.session['asi_session']
        },
        context_instance=RequestContext(request))


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
    template = loader.get_template("frontpage/home.html")
    feedurl = 'frontpage/feeds.html'
    feeds = EventLog.constructor(user_ids=friends)
    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'feedurl': feedurl,
        'feeds': feeds,
    })
    return HttpResponse(template.render(context))


@check_authentication
def profile(request, user_id=None):
    template = loader.get_template("frontpage/profile.html")

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
        avatar_url = '{0}{1}/large_thumbnail'.format(
            ASI_BASE_URL, user['avatar']['link']['href'])
    except (KeyError, TypeError):
        avatar_url = ''
    feedurl = 'frontpage/feeds.html'
    feeds = EventLog.constructor(user_ids=user_id)
    context = RequestContext(request, {
	'asi_session': request.session['asi_session'],
        'profile_user': user,
        'username': username,
        'realname': realname,
        'avatar_url': avatar_url,
        'template':'profile',
        'feedurl':feedurl,
        'feeds':feeds,
    })
    return HttpResponse(template.render(context))


def list_friends(request, user_id):
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

    for id_ in pending_friend_ids:
        pending = api.people.get(id_)
        pending['user_id'] = id_
        pending_requests.append(pending)

    template = loader.get_template("frontpage/friends.html")
    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'friends': friends,
        'requests': pending_requests,
        'profile_user': profile_user,
        'template': 'friends'
    })
    return HttpResponse(template.render(context))


def add_friend(request, user_id):
    print "add_friend called"
    session = request.session['asi_session']
    own_id = session.user_id
    print "adding friend: " + user_id
    session.add_friend(user_id)
    print "add returned"

    return HttpResponseRedirect(reverse("friends", args=[own_id]))


def registrations(request):
    template = loader.get_template("frontpage/registrations.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@check_authentication
def completed_courses(request, user_id):
    template = loader.get_template("frontpage/profile_courses_completed.html")

    asi_session = request.session['asi_session']
    profile_user = api.people.get(user_id)
    courses = api.people.get_completed_courses(user_id)

    context = RequestContext(request, {
        'asi_session': asi_session,
        'profile_user': profile_user,
        'courses': courses,
        'template': 'profile_courses_completed',
    })

    return HttpResponse(template.render(context))


@check_authentication
def friends_courses(request, user_id):
    asi_session = request.session['asi_session']
    profile_user = api.people.get(user_id)
    courses = utils.courses_taken_by_friends(user_id)

    return render_to_response(
        'frontpage/profile_courses_friends.html',
        {
            'profile_user': profile_user,
            'courses': courses,
            'asi_session': asi_session,
            'template': 'profile_courses_friends',
        },
        context_instance=RequestContext(request))


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
    courses = []

    for course_entry in coursedb:
        course_code = course_entry.course_code
        courses.append(api.course.get_course(course_code))

    template = loader.get_template("frontpage/profile_courses_planned.html")
    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'profile_user': user,
        'planned_courses': courses,
        'template': 'profile_courses_planned',
    })
    return HttpResponse(template.render(context))


def add_to_planned_courses(request):
    if request.method == "POST":
        course_code = request.POST.get('course_code', None)
        asi_session = request.session['asi_session']
        uid = asi_session.user_id

        if(course_code != None):
            course = PlannedCourse(course_code=course_code, user_id=uid)
            course.save()
            event = PlannedCourseEvent(course_code=course_code, user_id=uid)
            event.save()
            request.method = "GET"
            return HttpResponseRedirect(reverse("plannedcourses", args=[uid]))
        else:
            return HttpResponseBadRequest(
                "Could not add course to planned courses.")


def remove_planned_course(request):
    """
    this method removes a course from planned courses
    we use this method because the AJAX http DELETE does not work
    with all browsers
    """
    course_code = request.POST.get('course_code', None)
    asi_session = request.session['asi_session']
    uid = asi_session.user_id
    PlannedCourse.objects.filter(user_id=uid, course_code=course_code).delete()
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

    template = loader.get_template("frontpage/recommend_course.html")
    context = RequestContext(request, {
        'asi_session': asi_session,
        'friends': friends,
        'course': course
    })
    return HttpResponse(template.render(context))


def recommend_to_friends(request, coursecode):
    """
    This method takes a post form with friend id's and
    adds to their recommended courses.
    """
    res = request.POST
    print res

    return HttpResponseRedirect(reverse("home"))


def generalinfo(request):
    template = loader.get_template("frontpage/general_info.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def privacy(request):
    template = loader.get_template("frontpage/privacy.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


class SearchForm(forms.Form):
    # Required fields have * at the end of label
    query = forms.CharField(
        min_length=4,
        max_length=40,
        label="Keywords"
    )
    scope = forms.ChoiceField(
        [
            ('all', 'All content'),
            ('courses', 'Courses'),
            ('users', 'Users')
        ],
        label="Search option"
    )


@check_authentication
def search(request):
    template = loader.get_template("frontpage/search.html")
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

        context = RequestContext(request, {
            'searchform': searchform,
            'userresults': userresults,
            'courseresults': courseresults,
            'query': query,
            'asi_session': request.session['asi_session']
        })
    else:
        context = RequestContext(request, {
            'searchform': searchform,
            'asi_session': request.session['asi_session']
        })
    return HttpResponse(template.render(context))


def notifications(request):
    template = loader.get_template("frontpage/notifications.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def internal_error(request):
    return render_to_response(
        'frontpage/internal_error.html',
        context_instance=RequestContext(request))
