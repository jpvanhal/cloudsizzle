================
Deployment guide
================

This document describes how CloudSizzle system can be deployed for development and production.

Step 1. Start the required daemon processes
===========================================

Smart-M3
--------

First you will need to set up the environmental variable ``PIGLET_HOME``. That will tell Smart-M3 where the triple store should be stored in. The triple store is an Sqlite3 database file, which will be saved in ``$PIGLET_HOME/X``. Execute the command below and replace ``{path to piglet}`` with the directory you chose::

    export PIGLET_HOME={path to piglet}

In CloudSizzle's development server ``PIGLET_HOME`` is set to ``/srv/cloudsizzle/piglet``.

After that you can start up Smart-M3 by first starting ``sibd`` and then ``sib-tcp``. It might be a good idea to start these in `screen`_ with each process in a separate window.

.. _screen: http://www.gnu.org/software/screen/

ASI service knowledge processor
-------------------------------

ASI service knowledge processor handles all service request related to ASI like logging in and out, registering new user, managing user's friends, etc. You can start it by running::

    python -m cloudsizzle.asi.server

Again it would be good idea to start this in its own window in ``screen``.


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

``.kprc``::

    ('cloudsizzle', ('TCP', ('127.0.0.1', 10010)))

``django.wsgi``::

    import os
    import site
    import sys

    # Path to the virtual environment where CloudSizzle is installed
    VIRTUALENV_PATH = '/srv/cloudsizzle/demoenv'

    # Path to the CloudSizzle's project root directory
    CLOUDSIZZLE_ROOT = '/srv/cloudsizzle/demo'

    # The 'home' directory where .kprc file is located
    HOME_DIR = '/srv/cloudsizzle/demo/etc'

    # Map stdout to stderr. WSGI applications can not write to stdout.
    sys.stdout = sys.stderr

    site.addsitedir(os.path.join(VIRTUALENV_PATH, 'lib/python2.6/site-packages'))

    sys.path.append(os.path.join(CLOUDSIZZLE_ROOT, 'cloudsizzle'))
    sys.path.append(os.path.join(CLOUDSIZZLE_ROOT, 'cloudsizzle/studyplanner'))

    os.environ['HOME'] = HOME_DIR
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cloudsizzle.studyplanner.settings'

    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()

Add the following code to Apache's site configuration (e.g. ``httpd.conf``)::

    WSGIScriptAlias /demo /srv/cloudsizzle/demo/apache/django.wsgi
