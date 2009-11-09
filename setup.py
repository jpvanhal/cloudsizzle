#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

setup(
    name = 'cloudsizzle',
    fullname = 'CloudSizzle',
    version = '0.1',
    author = '',
    author_email = '',
    license = 'BSD',
    url = 'http://cloudsizzle.cs.hut.fi',
    description = 'Social study planner for Aalto University students',
    install_requires = ['Django >= 1.1', 'Scrapy == 0.7'],
    setup_requires=['nose>=0.11'],
    packages = find_packages(),
    test_suite = 'nose.collector'
)
