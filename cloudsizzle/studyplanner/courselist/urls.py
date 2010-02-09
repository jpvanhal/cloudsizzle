from django.conf.urls.defaults import *

urlpatterns = patterns('courselist.views',
    url(r'^$', 'list_faculties', name="courses"),
    (r'^(?P<faculty>[a-z]+)$', 'list_departments'),
    (r'^(?P<faculty>[a-z]+)/(?P<department>[a-zA-Z0-9-]+)$', 'list_courses'),
    (r'^(?P<faculty>[a-z]+)/(?P<department>[a-zA-Z0-9-]+)/(?P<course>[a-zA-Z0-9-\.]+)$', 'show_course'),
)
