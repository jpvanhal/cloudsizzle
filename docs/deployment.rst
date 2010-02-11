=================
Deployment manual
=================

This document describes how to install Cloudsizzle, and how it can be deployed for development and production.

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

Step 3. Install CloudSizzle
===========================

Installing an official release
------------------------------

Installing development version
------------------------------

Running the unit tests
----------------------


Step 4. Deploy the system
=========================

Deploying for development
-------------------------


Deploying for production
------------------------
