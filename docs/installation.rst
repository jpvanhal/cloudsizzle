==================
Installation guide
==================

This chapter will guide you to install CloudSizzle in to your system.


Step 1. Install required software
=================================

CloudSizzle has the following software requirements:

* Linux operating system
* `Python`_ 2.6 (other versions are not supported)
* `Smart-M3`_ 0.9.2 beta
* `setuptools`_
* `virtualenv`_ (optional, but recommended)

Install this software in to your system by following their installation
instructions.

.. _Python: http://www.python.org/
.. _Smart-M3: http://sourceforge.net/projects/smart-m3/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _virtualenv: http://pypi.python.org/pypi/virtualenv

Below is a list of Python libraries that Cloudsizzle uses. You do not need to
install these manually as they will be automatically installed with the
provided ``setuptools`` script.

* `Django`_ 1.1
* `Scrapy`_ 0.8
* `kpwrapper`_ 1.0.3
* `asilib`_ 1.0.2
* `asibsync`_ 0.9.3
* `MiniMock`_ 1.2 (optional, needed for unit tests)

.. _Django: http://www.djangoproject.com/
.. _Scrapy: http://www.scrapy.org/
.. _kpwrapper: http://pypi.python.org/pypi/kpwrapper
.. _asilib: http://pypi.python.org/pypi/asilib
.. _asibsync: http://pypi.python.org/pypi/asibsync
.. _MiniMock: http://pypi.python.org/pypi/MiniMock

Step 2. Change Python's default character encoding
==================================================

By default, when converting unicode strings to regular strings, Python uses
ASCII to encode the unicode string. This causes problems when the unicode
string contains characters not in ASCII. In order to work around this, Python's
default encoding needs to be changed. This can be done by creating a script
called ``sitecustomize.py``. It's a special script Python will try to run on
startup. It can be placed anywhere in Python's search path. A good place is in
the ``site-packages`` directory within your Python ``lib`` directory.

CloudSizzle uses UTF-8 encoding internally, so you should put this code in the
``sitecustomize.py`` script::

    import sys
    sys.setdefaultencoding('utf-8')

For more information about the subject, see the `chapter about Unicode`_ in
`Dive Into Python`_.

.. _chapter about Unicode: http://www.diveintopython.org/xml_processing/unicode.html
.. _Dive Into Python: http://www.diveintopython.org/


Step 3. Set up virtualenv (optional)
====================================

This step is optional, but strongly recommended. ``virtualenv`` is a makes it
possible to install Python modules in to a virtual environment. This makes it
possible to bring in the dependencies without messing up the rest of your
system. See ``virtualenv``'s `documentation`_ for more details about it.

Basic recipe is to first choose a directory where the virtual environment is
put in to. Then create a new virtual environment by running the command below
replacing ``{directory}`` with the chosen directory::

    virtualenv {directory}

The virtual environment can then be activated by running the following command::

    source {directory}/bin/activate

You can deactivate an active virtual environment by running::

    deactivate

.. _documentation: http://pypi.python.org/pypi/virtualenv/


Step 4. Install CloudSizzle
===========================

There are two ways to download and install CloudSizzle:

1. :ref:`install-release`
2. :ref:`install-dev`

.. _install-release:

Installing an official release
------------------------------

1. Download the latest official release from the `Download page`_. CloudSizzle
   is distributed as a source code tarball::

    wget http://cloudsizzle.cs.hut.fi/releases/cloudsizzle-X.X.tar.gz
    tar xvzf cloudsizzle-X.X.tar.gz

2. Copy ``cloudsizzle/settings.py.dev`` to ``cloudsizzle/settings.py`` and fill
   in your settings to that file.

3. Install Cloudsizzle as any other Python package with the help of
   ``setuptools``. This will also install all needed Python libraries::

    cd cloudsizzle-X.X
    python setup.py install

.. _Download page: http://cloudsizzle.cs.hut.fi/trac/wiki/Download


.. _install-dev:

Installing development version
------------------------------

1. Check out the latest development code from the Subversion repository (you
   might need to install `Subversion`_ first)::

    svn co http://cloudsizzle.cs.hut.fi/svn/trunk cloudsizzle-trunk

2. Copy ``cloudsizzle/settings.py.dev`` to ``cloudsizzle/settings.py`` and fill
   in your settings to that file.

3. Deploy the project in "Development mode". This will also install all needed
   Python libraries::

    cd cloudsizzle-trunk
    python setup.py develop

.. _Subversion: http://subversion.tigris.org/


Step 5. Run the unit tests
==========================

In order to ensure that everything is installed correctly, you should run the
unit tests. You can run them with the following command in the project root::

    python setup.py test

This will not, however, run Django's unit tests. Those can be run by changing
to ``cloudsizzle/studyplanner`` directory inside project root and running::

    python manage.py test
