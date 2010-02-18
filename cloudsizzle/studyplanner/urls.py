from django.conf.urls.defaults import url, patterns, include
from django.conf import settings

urlpatterns = patterns('',
    url(
        r'^$',
        'studyplanner.frontpage.views.index',
        name='frontpage'
    ),

    url(
        r'^session/logout/$',
        'studyplanner.frontpage.views.logout',
        name='logout_user'
    ),

    url(
        r'^home/$',
        'studyplanner.frontpage.views.home',
        name='home'
    ),

    url(
        r'^welcome/$',
        'studyplanner.frontpage.views.welcome',
        name='welcome'
    ),

    url(
        r'^profile/add_friend/(?P<user_id>[a-zA-Z0-9-_]+)/$',
        'studyplanner.frontpage.views.add_friend',
        name='addfriend'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/courses/completed/$',
        'studyplanner.frontpage.views.completed_courses',
        name='completed_courses'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/courses/friends/$',
        'studyplanner.frontpage.views.friends_courses',
        name='friendscourses'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/courses/planned/$',
        'studyplanner.frontpage.views.planned_courses',
        name='plannedcourses'
    ),

    url(
        r'^profile/courses/planned/add/$',
        'studyplanner.frontpage.views.add_to_planned_courses',
        name='add_to_planned_courses'
    ),

    url(
        r'^profile/courses/planned/remove/$',
        'studyplanner.frontpage.views.remove_planned_course',
        name='remove_from_planned_courses'
    ),

    url(
        r'^profile/$',
        'studyplanner.frontpage.views.profile',
        name='profile'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)$',
        'studyplanner.frontpage.views.profile',
        name='profile'
    ),

    url(
        r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/friends/$',
        'studyplanner.frontpage.views.list_friends',
        name='friends'
    ),

    url(
        r'^registrations/$',
        'studyplanner.frontpage.views.registrations',
        name='registrations'
    ),

    url(
        r'^recommendcourse/(?P<coursecode>[a-zA-Z0-9-\.]+)$',
        'studyplanner.frontpage.views.recommendcourse',
        name='recommendcourse'
    ),

    url(
        r'^recommendtofriends/(?P<coursecode>[a-zA-Z0-9-\.]+)$',
        'studyplanner.frontpage.views.recommend_to_friends',
        name='recommendtofriends'
    ),

    url(
        r'^search/$',
        'studyplanner.frontpage.views.search',
        name='search'
    ),

    url(
        r'^internalerror/$',
        'studyplanner.frontpage.views.internal_error',
        name='internalerror'
    ),

    url(r'^courses/', include('courselist.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
    ))
