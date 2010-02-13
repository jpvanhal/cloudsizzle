================
Deployment guide
================

This document describes how CloudSizzle system can be deployed for development and production.

Step 1. Start the required daemon processes
===========================================

It might be a good idea to start these processes in a ``screen``.

Smart-M3
--------

You can run Smart-M3 by executing the following commands::

    export PIGLET_HOME=<path to piglet>
    sibd &
    sib-tcp &

ASI service knowledge processor
-------------------------------

ASI service knowledge processor handles all service request related to ASI like logging in and out, registering new user, managing user's friends, etc. You can start it by running::

    python -m cloudsizzle.asi.server


Step 2. Deploy the Django application
=====================================

Deploying for development
-------------------------

1. Go to ``cloudsizzle/studyplanner`` directory inside project root.

2. Edit ``settings.py`` and make sure that the database settings are correct.

3. Execute the command below in order to create the database tables::

    python manage.py syncdb

4. Execute the command below in order to start development server::

    python manage.py runserver

5. Go to http://localhost:8000 with your web browser.


Deploying with Apache and mod_wsgi
----------------------------------

``django.wsgi``::

    import site
    import os
    import sys

    os.environ['HOME'] = '/srv/cloudsizzle/demo/etc'

    # Map stdout to stderr. WSGI applications can not write to stdout.
    sys.stdout = sys.stderr

    site.addsitedir('/srv/cloudsizzle/demoenv/lib/python2.6/site-packages')

    sys.path.append('/srv/cloudsizzle/demo/cloudsizzle')
    sys.path.append('/srv/cloudsizzle/demo/cloudsizzle/studyplanner')

    os.environ['DJANGO_SETTINGS_MODULE'] = 'cloudsizzle.studyplanner.settings'

    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()

Apache's site configuration::

    WSGIScriptAlias /demo /srv/cloudsizzle/demo/apache/django.wsgi
