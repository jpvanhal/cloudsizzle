from django.conf.urls.defaults import *
from django.conf import settings
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

    #courselist application for the first demonstration
    #url(r'^courses/', include('courselist.urls')),
    #url(r'^completed/', 'completedstudies.views.index'),

    #Login application, demo as well
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': 'C:/Users/kristoffer/Documents/studier/T-76.4115/reposit-co/trunk/cloudsizzle/studyplanner/static'}),
                            )
    
