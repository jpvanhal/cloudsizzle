from django.conf.urls.defaults import *

urlpatterns = patterns('courselist.views',
    (r'^$', 'list_faculties'),
    (r'^(?P<faculty>[a-z]+)$', 'list_departments'),
    (r'^(?P<faculty>[a-z]+)/(?P<department>[a-z0-9-]+)$', 'list_courses'),
    (r'^(?P<faculty>[a-z]+)/(?P<department>[a-z0-9-]+)/(?P<course>[a-z0-9-\.]+)$', 'show_course'),
)
