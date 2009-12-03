from django.conf.urls.defaults import *

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
    
    #courselist application for the first demonstration
    (r'^$', 'studyplanner.main.views.courselist'),
    (r'^list/$', 'studyplanner.courselist.views.courselist'),
    
    #Login application, demo as well
    (r'^session/$', 'studyplanner.session.views.index'),
)
