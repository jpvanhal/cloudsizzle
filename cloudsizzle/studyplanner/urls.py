from django.conf.urls.defaults import *
from django.conf import settings
import socket
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^cloudsizzle/', include('cloudsizzle.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    url(r'^$', 'studyplanner.frontpage.views.index', name='frontpage'),
    url(r'^session/logout/+?', 'studyplanner.frontpage.views.logout', name='logout_user'),
    #user list
    #url(r'^users/$', 'studyplanner.userlist.views.list_users', name='list of users'),
    
    url(r'^home/$', 'studyplanner.frontpage.views.home', name='home'),

    url(r'^welcome/?$', 'studyplanner.frontpage.views.welcome', name='welcome'),

    url(r'^profile$', 'studyplanner.frontpage.views.profile', name='profileown'),
    url(r'^profile/add_friend/(?P<user_id>[a-zA-Z0-9-_]+)/?$', 'studyplanner.frontpage.views.add_friend', name='addfriend'),
    url(r'^profile/friendscourses/?$', 'studyplanner.frontpage.views.friendscourses', name='friendscourses'),
    url(r'^profile/plannedcourses/?$', 'studyplanner.frontpage.views.planned_courses', name='plannedcourses'),
    url(r'^profile/removeplannedcourses/?$', 'studyplanner.frontpage.views.remove_planned_course', name='removefromplannedcourses'),
    url(r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)$', 'studyplanner.frontpage.views.profile', name='profile'),
    url(r'^profile/(?P<user_id>[a-zA-Z0-9-_]+)/friends/$', 'studyplanner.frontpage.views.friends', name='friends'),
    url(r'^feed/(?P<user_id>[a-zA-Z0-9-_]+)$', 'studyplanner.frontpage.views.feed', name='feed'),
    url(r'^registrations/$', 'studyplanner.frontpage.views.registrations', name='registrations'),

    url(r'^completedstudies/$', 'studyplanner.frontpage.views.completedstudies', name='completedstudies'),
    #url(r'^coursesfaculty/$', 'studyplanner.frontpage.views.coursesfaculty', name='coursesfaculty'),
    #url(r'^coursesdepartment/$', 'studyplanner.frontpage.views.coursesdepartment', name='coursesdepartment'),
    #url(r'^course/$', 'studyplanner.frontpage.views.course', name='course'),
    #url(r'^recommendedcourse/$', 'studyplanner.frontpage.views.recommendedcourse', name='recommendedcourse'),
    #url(r'^generalinfo/$', 'studyplanner.frontpage.views.generalinfo', name='generalinfo'),
    #url(r'^privacy/$', 'studyplanner.frontpage.views.privacy', name='privacy'),
    url(r'^search$', 'studyplanner.frontpage.views.search', name='search'),
    #url(r'^notifications/$', 'studyplanner.frontpage.views.notifications', name='notifications'),

    url(r'^courses/', include('courselist.urls')),
    #url(r'^completed/', 'completedstudies.views.index'),

    #Login application, demo as well
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)

if socket.gethostname() == 'cloudsizzle.cs.hut.fi': 
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
                            )
    
