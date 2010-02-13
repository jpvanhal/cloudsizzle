#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

setup(
    name = 'cloudsizzle',
    fullname = 'CloudSizzle',
    version = '0.1',
    author = 'CloudSizzle Team',
    author_email = 'cloudsizzle@cs.hut.fi',
    license = 'MIT',
    url = 'http://cloudsizzle.cs.hut.fi',
    description = 'Social study planner for Aalto University students',
    install_requires = [
        'Django >= 1.1',
        'Scrapy == 0.8',
        'kpwrapper >= 1.0.3',
        'asilib >= 1.0.2',
        'asibsync >= 1.0.2',
    ],
    packages = find_packages(),
    include_package_data = True,
    test_suite = 'cloudsizzle.tests.suite',
    tests_require = [
        'MiniMock >= 1.2',
    ],
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
