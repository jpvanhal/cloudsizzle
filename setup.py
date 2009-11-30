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
    license = 'MIT',
    url = 'http://cloudsizzle.cs.hut.fi',
    description = 'Social study planner for Aalto University students',
    install_requires = [
        'Django >= 1.1',
        'Scrapy == 0.7',
        'kpwrapper >= 0.9.2',
    ],
    packages = find_packages(),
    test_suite = 'cloudsizzle.tests.suite',
    dependency_links = [
        'http://public.futurice.com/~ekan/eggs',
        'http://ftp.edgewall.com/pub/bitten/',
    ],
    extras_require = {
        'Bitten': ['bitten'],
    },
    entry_points = {
        'distutils.commands': [
            'unittest = bitten.util.testrunner:unittest [Bitten]'
        ],
    },
)
