==================
Installation guide
==================

Requirements
============

Required software
-----------------

* `Python`_ 2.6 (other versions are not supported)

* `Smart-M3`_ 0.9.2 beta

* `setuptools`_

* `virtualenv`_ (optional, but recommended)

Required Python libraries
-------------------------

Below is a list of Python libraries that Cloudsizzle uses. You do not need to install these manually (with the exception of kpwrapper). They will be automatically installed with the provided setuptools script.

* `Django`_ 1.1

* `Scrapy`_ 0.8

* `kpwrapper`_ 1.0.2

  * Please do not use the official version. It will not work. You will need to apply `this patch`_ that fixes a bug in node type handling, or install the `patched egg`_.

* `asilib`_ 1.0.2

* `asibsync`_ 1.0.2

.. _Python: http://www.python.org/
.. _Smart-M3: http://sourceforge.net/projects/smart-m3/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Django: http://www.djangoproject.com/
.. _Scrapy: http://www.scrapy.org/
.. _kpwrapper: http://pypi.python.org/pypi/kpwrapper
.. _this patch: http://cloudsizzle.cs.hut.fi/trac/raw-attachment/ticket/276/fix_tuple_to_triple_node_type_handling.diff
.. _patched egg: http://cloudsizzle.cs.hut.fi/trac/raw-attachment/ticket/276/kpwrapper-1.0.2-py2.6.egg
.. _asilib: http://pypi.python.org/pypi/asilib
.. _asibsync: http://pypi.python.org/pypi/asibsync


Step 1. Install required software
=================================


Step 2. Set up virtualenv (optional)
====================================

This step is optional, but strongly recommended. ``virtualenv`` is a makes it possible to install Python modules in to a virtual environment. This makes it possible to bring in the dependencies without messing up the rest of your system. See ``virtualenv``'s `documentation`_ for more details about it.

Basic recipe is to first choose a directory where the virtual environment is put in to. Then create a new virtual environment by running the command below replacing ``{directory}`` with the chosen directory::

    virtualenv {directory}

The virtual environment can then be activated by running the following command::

    source {directory}/bin/activate

You can deactivate an active virtual environment by running::

    deactivate

.. _documentation: http://pypi.python.org/pypi/virtualenv/


Step 3. Install CloudSizzle
===========================

There are two ways to download and install CloudSizzle:

1. :ref:`install-release`
2. :ref:`install-dev`

.. _install-release:

Installing an official release
------------------------------

1. Download the latest official release from the `Download page`_. CloudSizzle is distributed as a source code tarball::

    wget http://cloudsizzle.cs.hut.fi/releases/cloudsizzle-X.X.tar.gz
    tar xvzf cloudsizzle-X.X.tar.gz

2. Copy `cloudsizzle/settings.py.dev` to `cloudsizzle/settings.py` and fill in your settings to that file.

3. Install Cloudsizzle as any other Python package with the help of ``setuptools``. This will also install all needed Python libraries::

    cd cloudsizzle-X.X
    python setup.py install

.. _install-dev:

Installing development version
------------------------------

1. Check out the latest development code from the Subversion repository (you might need to install Subversion first)::

    svn co http://cloudsizzle.cs.hut.fi/svn/trunk cloudsizzle-trunk

2. Copy `cloudsizzle/settings.py.dev` to `cloudsizzle/settings.py` and fill in your settings to that file.

3. Deploy the project in "Development mode". This will also install all needed Python libraries::

    cd cloudsizzle-trunk
    python setup.py develop


Running the unit tests
======================

You can run the unit tests by running the following command in the project root::

    python setup.py unittest

This will not, however, run Django's unit tests. They can be run by changing to `cloudsizzle/studyplanner` directory inside project root and running::

    python manage.py test
