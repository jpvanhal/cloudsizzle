from django.conf.urls.defaults import *

urlpatterns = patterns('courselist.views',
    url(r'^$', 'list_faculties', name="courses"),
    (r'^(?P<faculty>[a-z]+)$', 'list_departments'),
    (r'^(?P<faculty>[a-z]+)/(?P<department>[a-zA-Z0-9-]+)$', 'list_courses'),
    url(r'^(?P<faculty>[a-z]+)/(?P<department>[a-zA-Z0-9-]+)/(?P<course>[a-zA-Z0-9-\.]+)$', 'show_course',name="show_course"),
    # This assumes that all courses contain dash, otherwise it will
    # match the faculty view. This is neede because search results
    # do not give faculty or department. Perhaps the search should
    # be fixed instead...
    url(r'^(?P<course>[a-zA-Z0-9-\.]+)$', 'show_bare_course', name="show_bare_course"),
)
