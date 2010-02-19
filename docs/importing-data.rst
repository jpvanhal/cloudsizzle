==============
Importing data
==============

This chapter describes how to import data from various sources to SIB.


Aalto Social Interface
======================

The people and their friends from Aalto Social Interface can be imported with
the following command::

    python -m cloudsizzle.asi.importer

Please note that this does not work correctly if there is old people
information in SIB: outdated information is not removed from SIB.


Screen scrapers
===============

Screen scrapers are controlled with the ``scripts/scrapy-ctl.py`` script. They
can be used for scraping data from Noppa and WebOodi.

Course information from Noppa can be scraped with::

    python scripts/scrapy-ctl.py crawl \
    --settings cloudsizzle.scrapers.noppa.settings noppa.tkk.fi

Student's completed studies can be scraped with::

    python scripts/scrapy-ctl.py crawl \
    --settings cloudsizzle.scrapers.oodi.settings oodi.tkk.fi \
    --set ASI_USER_ID=<user_id> \
    --set TKK_WEBLOGIN_USERNAME=<username> \
    --set TKK_WEBLOGIN_PASSWORD=<password>

Note that you need to pass student's Weblogin username and password and an ASI
user id as parameters to the command. The scraped completed courses will be
linked with the given ASI user id.

You can also skip any of these parameters. In that case you will be prompted to
enter them.
