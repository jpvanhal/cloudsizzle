from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('courselist.views',

    url(
        r'^$',
        'list_faculties',
        name="courses"
    ),

    url(
        r'^(?P<faculty>[a-z]+)$',
        'list_departments',
        name='show_faculty'
    ),

    url(
        r'^(?P<faculty>[a-z]+)/(?P<department>[a-zA-Z0-9-]+)$',
        'list_courses',
        name='show_department'
    ),

    url(
        r'^(?P<faculty>[a-z]+)/(?P<department>[a-zA-Z0-9-]+)/'
        r'(?P<course>[a-zA-Z0-9-\.]+)$',
        'show_course',
        name="show_course"
    ),
)
