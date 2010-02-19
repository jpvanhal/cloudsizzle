================
Deployment guide
================

This chapter describes how CloudSizzle system can be deployed for development
and production.

Step 1. Start the required daemon processes
===========================================

Smart-M3
--------

First you will need to set up the environmental variable ``PIGLET_HOME``. That
will tell Smart-M3 where the triple store should be stored in. The triple store
is an Sqlite3 database file, which will be saved in ``$PIGLET_HOME/X``. Execute
the command below and replace ``{path to piglet}`` with the directory you
chose::

    export PIGLET_HOME={path to piglet}

In CloudSizzle's development server ``PIGLET_HOME`` is set to
``/srv/cloudsizzle/piglet``.

After that you can start up Smart-M3 by first starting ``sibd`` and then
``sib-tcp``. It might be a good idea to start these in `screen`_ with each
process in a separate window.

If you receive error messages about DBUS, it is probably because you are trying
to start these processes by SSH. Note that if you are using X tunneling with
SSH, everything seems to be working okay, but SIB is actually using your local
DBUS instead of the DBUS in the server you are connected to. In order to make
SIB use the DBUS in the server, you should execute the following commands::

    $ eval $(dbus-launch --sh-syntax)
    $ export BUS_SESSION_BUS_ADDRESS
    $ export DBUS_SESSION_BUS_PID

.. _screen: http://www.gnu.org/software/screen/

ASI service knowledge processor
-------------------------------

ASI service knowledge processor handles all service request related to ASI like
logging in and out, registering new user, managing user's friends, etc. You can
start it by running::

    python -m cloudsizzle.asi.server

Again it would be good idea to start this in its own window in ``screen``.


Step 2. Deploy the Django application
=====================================

You can deploy the django application in two ways. First alternative is a good
choice when you are developing the application, and the other one is for
deploying the system for production. The first steps in both of these
alternatives are common:

1. Go to ``cloudsizzle/studyplanner`` directory inside project root.

2. Edit ``settings.py`` and make sure that the database settings are correct.

3. Execute the command below in order to create the database tables::

    python manage.py syncdb

4. Create a new file ``.kprc`` in the home directory of the user who is going
   to be running the system. Put the following code in this file::

        ('cloudsizzle', ('TCP', ('127.0.0.1', 10010)))

   In this code ``'cloudsizzle'`` is the name of the smart space in SIB.
   According to our testing it does not matter what name you are using: SIB
   always uses the same smart space regardless of smart space name.
   ``'127.0.0.1'`` is the IP address where SIB is running. ``127.0.0.1`` is the
   correct address here if you are running Django application on the same
   server as SIB. Finally ``10010`` is the TCP port where SIB is running. By
   default SIB uses ``10010``.


Deploying for development
-------------------------

This section describes how to start Django's development server. This
deployment option is ideal when you are developing the system.

1. Execute the command below in order to start development server::

    python manage.py runserver

2. Go to http://localhost:8000 with your web browser.

For more information, see the section about ``runserver`` command in
`Django's documentation`_.

.. _Django's documentation: http://docs.djangoproject.com/en/dev/ref/django-admin/#runserver-port-or-ipaddr-port


Deploying with Apache and mod_wsgi
----------------------------------

This section describes how to run the Django application with `Apache`_ and
`mod_wsgi`_. This deployment option is ideal, when you want to deploy the
system for production. This method is also the one used on the `demo site`_.
We will use the demo site configuration in CloudSizzle's development server as
an example from now on. This method requires that you have Apache and mod_wsgi
installed.

The demo site is setup to our development server so that the code is checked
out by Subversion in ``/srv/cloudsizzle/demo``. We also use an virtual
environment, which is located in ``/srv/cloudsizzle/demoenv``. As Apache does
not seem to have a home directory, we have put ``.kprc`` file in
``/srv/cloudsizzle/demo/etc`` and set the ``$HOME`` environmental variable
accordingly.

The first thing to do is to add the following code to Apache's site
configuration (e.g. ``httpd.conf``). In our development server this is put in
``/etc/httpd/conf.d/demo.conf``::

    WSGIScriptAlias /demo /srv/cloudsizzle/demo/apache/django.wsgi

    Alias /static /srv/cloudsizzle/demo/cloudsizzle/studyplanner/static
    <Location "/static">
        SetHandler None
    </Location>

In the first line after the WSGIScriptAlias the first bit is the url where the
application is served at. The second bit is the location of the WSGI application
script, which we will be creating next. The rest of the code sets up an alias
for static files so that they are server directly by Apache and not through
Django. Change the path in the Alias directive to suit your setup.

The next thing to do is to create the WSGI application. Create the file
mentioned in the second part of ``WSGIScriptAlias`` and put the following code
in there (remember to change the constants to fit to your setup)::

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

Please refer to the chapter `How to use Django with Apache and mod_wsgi`_ in
Django's documentation for more detailed instructions.

.. _Apache: http://httpd.apache.org/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _demo site: http://cloudsizzle.cs.hut.fi/demo
.. _How to use Django with Apache and mod_wsgi: http://docs.djangoproject.com/en/1.1/howto/deployment/modwsgi/
