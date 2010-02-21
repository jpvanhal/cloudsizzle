# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2010 CloudSizzle Team
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
Frontpage view that handles most of the study planner. Probably needs to be
split into individual applications or files.

"""
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, Http404
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django import forms
from cloudsizzle.studyplanner.common.forms import LoginForm, RegisterForm
from cloudsizzle.studyplanner.common.planner_session import \
    is_authenticated, authenticate, check_authentication
from cloudsizzle.studyplanner.events.event import EventLog
from cloudsizzle import api
from cloudsizzle.studyplanner.events.models import \
    PlannedCourse as PlannedCourseEvent, NewFriendEvent
from cloudsizzle.studyplanner.frontpage.models import \
    PlannedCourse, RecommendedCourse
from cloudsizzle.asi.client import TimeOutError
from cloudsizzle.studyplanner.courselist import utils
from cloudsizzle.settings import ASI_BASE_URL

# For injecting error messages to registration form if registration failed
# This is generally forms internal API.
from django.forms.util import ErrorList


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
        print "register view posted"
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
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
            try:
                api.people.create(username, password, email)
            except ValueError as error:
                register_form._errors['username'] = ErrorList(error.args)
                # And fall down to render_to_response
            else:
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
        print "register view getted"
        register_form = RegisterForm()

    login_form = LoginForm()

    return render_to_response(
        'frontpage/login-register.html',
        {
            'loginform': login_form,
            'registerform': register_form
        },
        context_instance=RequestContext(request))


def login(request):
    # Django standard form processing pattern:
    # User submitted form by POST
    if request.method == 'POST':
        print "login view posted"
        login_form = LoginForm(request.POST)

        if login_form.is_valid() and request.POST['submit'] == 'Login':
            # Use API to try to login
            # Write results to form if failed
            # Otherwise show home here
            print "login form was valid"
            username = login_form.cleaned_data['login_username']
            password = login_form.cleaned_data['login_password']
            try:
                print 'calling authenticate'
                authenticate(request, username, password)
                print 'authenticate returned'
            except api.LoginFailed as message:
                # assume that this always means bad username/password
                message = u'Please check your username and password'
                login_form._errors['login_username'] = ErrorList([message])
            except TimeOutError:
                print "Timeout while authenticating"
                message = u'A timeout occurred. Please try again.'
                login_form._errors['login_username'] = ErrorList([message])
            else:
                return HttpResponseRedirect(reverse('home'))
    else:
        print "login view getted"
        login_form = LoginForm()

    return render_to_response('frontpage/login.html',
        {'loginform': login_form}
    )


@check_authentication
def welcome(request):
    """Welcome page, shown when user has registered."""
    return render_to_response(
        'frontpage/welcome.html',
        {
            'asi_session': request.session['asi_session']
        },
        context_instance=RequestContext(request))


@check_authentication
def logout(request):
    """Log the user out. Removes ASI connection from session"""
    print 'Closing session'
    request.session['asi_session'].close()
    print 'Session closed'
    del request.session['asi_session']

    return HttpResponseRedirect(reverse('frontpage'))


@check_authentication
def home(request):
    asi_session = request.session['asi_session']
    user_id = asi_session.user_id
    friends = api.people.get_friends(user_id)
    template = loader.get_template("frontpage/home.html")
    feedurl = 'frontpage/feeds.html'
    feeds = EventLog.constructor(user_ids=friends)
    notification_num = RecommendedCourse.get_notification_num(user_id=user_id)
    pending_friend_ids = asi_session.get_pending_friend_requests()
    friend_requests_num = len(pending_friend_ids)

    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'feedurl': feedurl,
        'feeds': feeds,
        'notification_num':notification_num,
        'friend_requests_num': friend_requests_num
    })
    return HttpResponse(template.render(context))

@check_authentication
def delete_notifications(request):
    asi_session = request.session['asi_session']
    user_id = asi_session.user_id
    course_name = request.POST["plan course"]
    course_code = str(course_name).split('/')[-1]
    RecommendedCourse.delete_course(user_id=user_id, course_code=course_code)

    if "plan_to_take" in request.POST:
        forward_url = request.POST["plan course"]
    elif "ignore" in request.POST:
        forward_url =  reverse("notifications")
    return HttpResponseRedirect(forward_url)

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

    # mutual friends
    mutual_friends = []
    mutual_friend_ids = api.people.get_mutual_friends(
                                                asi_session.user_id, user_id)
    for mutual_friend_id in mutual_friend_ids:
        mutual_friends.append(api.people.get(mutual_friend_id))

    # mutual courses
    mutual_courses = []
    mutual_course_ids = utils.mutual_courses(
                                        asi_session.user_id, user_id)

    for mutual_course_id in mutual_course_ids:
        try:
            mutual_courses.append(api.course.get_course(mutual_course_id))
        except Exception:
            # Just ignore invalid course codes
            pass

    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'ASI_BASE_URL': ASI_BASE_URL,
        'profile_user': user,
        'username': username,
        'realname': realname,
        'avatar_url': avatar_url,
        'template': 'profile',
        'feedurl': feedurl,
        'feeds': feeds,
        'mutual_friends': mutual_friends,
        'mutual_courses': mutual_courses
    })
    return HttpResponse(template.render(context))


@check_authentication
def list_friends(request, user_id):
    asi_session = request.session['asi_session']

    try:
        profile_user = api.people.get(user_id)
    except api.people.UserDoesNotExist:
        raise Http404


    friend_ids = api.people.get_friends(user_id)
    friends = []

    for friend_id in friend_ids:
        try:
            friend = api.people.get(friend_id)
            friend['num_mutual_friends'] = len(api.people.get_mutual_friends(
                                                asi_session.user_id, friend_id))
            friend['num_mutual_courses'] = len(utils.mutual_courses(
                                                asi_session.user_id, friend_id))
            friends.append(friend)
        except api.people.UserDoesNotExist:
            # Invalid friend relationship where friend does not exist in ASI
            pass

    pending_requests = []
    if asi_session.user_id == user_id:
        pending_friend_ids = asi_session.get_pending_friend_requests()

        for friend_id in pending_friend_ids:
            try:
                pending = api.people.get(friend_id)
                pending['num_mutual_friends'] = len(api.people.get_mutual_friends(
                                                    asi_session.user_id, friend_id))
                pending['num_mutual_courses'] = len(utils.mutual_courses(
                                                    asi_session.user_id, friend_id))
                pending_requests.append(pending)
            except api.people.UserDoesNotExist:
                # Invalid friend relationship where friend does not exist in ASI
                pass

    template = loader.get_template("frontpage/friends.html")
    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'ASI_BASE_URL': ASI_BASE_URL,
        'friends': friends,
        'requests': pending_requests,
        'profile_user': profile_user,
        'template': 'friends'
    })
    return HttpResponse(template.render(context))


@check_authentication
def add_friend(request, user_id):
    print "add_friend called"
    session = request.session['asi_session']
    own_id = session.user_id
    print "adding friend: " + user_id
    session.add_friend(user_id)
    print "add returned"
    event = NewFriendEvent(new_friend=user_id, user_id=own_id)
    event.save()
    return HttpResponseRedirect(reverse("friends", args=[own_id]))


@check_authentication
def remove_friend(request, user_id):
    session = request.session['asi_session']
    own_id = session.user_id
    session.remove_friend(user_id)
    # No event for this is defined
    return HttpResponseRedirect(reverse("friends", args=[own_id]))


@check_authentication
def completed_courses(request, user_id):
    template = loader.get_template("frontpage/profile_courses_completed.html")

    try:
        profile_user = api.people.get(user_id)
    except api.people.UserDoesNotExist:
        raise Http404

    courses = api.people.get_completed_courses(user_id)

    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'profile_user': profile_user,
        'courses': courses,
        'template': 'profile_courses_completed',
    })

    return HttpResponse(template.render(context))


@check_authentication
def friends_courses(request, user_id):
    try:
        profile_user = api.people.get(user_id)
    except api.people.UserDoesNotExist:
        raise Http404

    courses = utils.courses_taken_by_friends(user_id)

    return render_to_response(
        'frontpage/profile_courses_friends.html',
        {
            'profile_user': profile_user,
            'courses': courses,
            'asi_session': request.session['asi_session'],
            'template': 'profile_courses_friends',
        },
        context_instance=RequestContext(request))


@check_authentication
def planned_courses(request, user_id):
    try:
        user = api.people.get(user_id)
    except api.people.UserDoesNotExist:
        raise Http404

    coursedb = PlannedCourse.objects.filter(user_id=user_id)
    courses = []

    for course_entry in coursedb:
        course_code = course_entry.course_code
        try:
            course_info = api.course.get_course(course_code)
            course_info['friends'] = utils.count_friends_taking_course(user_id, course_code)
            courses.append(course_info)
        except Exception:
            # Just ignore invalid course codes.
            pass

    template = loader.get_template("frontpage/profile_courses_planned.html")
    context = RequestContext(request, {
        'asi_session': request.session['asi_session'],
        'profile_user': user,
        'planned_courses': courses,
        'template': 'profile_courses_planned',
    })
    return HttpResponse(template.render(context))


@check_authentication
def add_to_planned_courses(request):
    if request.method == "POST":
        course_code = request.POST.get('course_code', None)
        asi_session = request.session['asi_session']
        uid = asi_session.user_id

        if(course_code != None):
            course = PlannedCourse(course_code=course_code, user_id=uid)
            #course_code and user_id is unique together so this might throw
            # an integrity error, the check should be handled by the userinterface
            #too
            try:
                course.save()
            except IntegrityError:
                return HttpResponseBadRequest(
                    "The course is already in planned courses")

            event = PlannedCourseEvent(course_code=course_code, user_id=uid)
            event.save()
            request.method = "GET"
            return HttpResponseRedirect(reverse("plannedcourses", args=[uid]))
        else:
            return HttpResponseBadRequest(
                "Could not add course to planned courses.")


@check_authentication
def remove_planned_course(request):
    """
    this method removes a course from planned courses
    we use this method because the AJAX http DELETE does not work
    with all browsers
    """
    if request.method == "POST":
        course_code = request.POST.get('course_code', None)
    elif request.method == "GET":
        course_code = request.GET.get('course_code', None)
    asi_session = request.session['asi_session']
    uid = asi_session.user_id
    PlannedCourse.objects.filter(user_id=uid, course_code=course_code).delete()
    return HttpResponseRedirect(reverse("plannedcourses", args=[uid]))


@check_authentication
def recommendcourse(request, course_code):
    asi_session = request.session['asi_session']

    friend_ids = api.people.get_friends(asi_session.user_id)
    friends = []

    for friend_id in friend_ids:
        try:
            friend = api.people.get(friend_id)
            friends.append(friend)
        except api.people.UserDoesNotExist:
            pass

    try:
        course = api.course.get_course(course_code)
    except Exception:
        raise Http404

    template = loader.get_template("frontpage/recommend_course.html")
    context = RequestContext(request, {
        'ASI_BASE_URL': ASI_BASE_URL,
        'asi_session': asi_session,
        'friends': friends,
        'course': course
    })
    return HttpResponse(template.render(context))


@check_authentication
def recommend_to_friends(request, course_code):
    """
    This method takes a post form with friend id's and
    adds to their recommended courses.
    """
    asi_session = request.session['asi_session']
    user_id = asi_session.user_id

    for friend_id, value in request.POST.iteritems():
        if value == "on":
            recommended_course = RecommendedCourse(
                                    user_recommending = user_id,
                                    user_recommended = friend_id,
                                    course_code = course_code
                                    )
            try:
                recommended_course.save()
            except IntegrityError:
                pass

    return HttpResponseRedirect(reverse("home"))


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
    asi_session = request.session['asi_session']
    if searchform.is_valid():
        query = searchform.cleaned_data['query']
        scope = searchform.cleaned_data['scope']
        userresults = []
        courseresults = []

        if scope == 'all' or scope == 'users':
            for userid in api.people.search(query):
                try:
                    details = api.people.get(userid)
                except api.people.UserDoesNotExist:
                    continue
                # Note that is a set, template gets to count them
                details['mutual_friends'] = api.people.get_mutual_friends(
                                            asi_session.user_id, userid)
                details['mutual_courses'] = utils.mutual_courses(
                                            asi_session.user_id, userid)
                userresults.append(details)
        if scope == 'all' or scope == 'courses':
            for coursecode in api.course.search(query):
                try:
                    details = api.course.get_course(coursecode)
                except Exception:
                    # Just ignore invalid course codes.
                    continue
                details['friendcount'] = utils. \
                    count_friends_taking_course(asi_session.user_id, coursecode)
                courseresults.append(details)

        context = RequestContext(request, {
            'ASI_BASE_URL': ASI_BASE_URL,
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


def internal_error(request):
    return render_to_response(
        'frontpage/internal_error.html',
        context_instance=RequestContext(request))

# Below this line are only mockups

def registrations(request):
    template = loader.get_template("frontpage/registrations.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def notifications(request):
    asi_session = request.session['asi_session']

    asi_session = request.session['asi_session']
    user_id = asi_session.user_id
    notifications = EventLog.get_notifications(user_id)

    pending_friend_ids = asi_session.get_pending_friend_requests()
    pending_requests = []

    for id_ in pending_friend_ids:
        try:
            pending = api.people.get(id_)
            pending_requests.append(pending)
        except api.people.UserDoesNotExist:
            pass

    template = loader.get_template("frontpage/notifications.html")
    context = RequestContext(request, {
                'ASI_BASE_URL': ASI_BASE_URL,
                'asi_session': asi_session,
                'requests': pending_requests,
                'notifications': notifications
    })
    return HttpResponse(template.render(context))


def privacy(request):
    template = loader.get_template("frontpage/privacy.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
