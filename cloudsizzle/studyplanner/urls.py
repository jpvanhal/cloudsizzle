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
    
    #user list
    url(r'^users/$', 'studyplanner.userlist.views.list_users', name='list of users'),

    #courselist application for the first demonstration
    #url(r'^courses/', include('courselist.urls')),
    #url(r'^completed/', 'completedstudies.views.index'),

    #Login application, demo as well
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)

if socket.gethostname() == 'cloudsizzle.cs.hut.fi': 
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
                            )
    
