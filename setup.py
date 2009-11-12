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
    install_requires = ['Django >= 1.1', 'Scrapy == 0.7'],
    packages = find_packages(),
    test_suite = 'cloudsizzle.tests.suite',
    tests_require = [
        'bitten',
    ],
    entry_points = {
        'distutils.commands': [
            'unittest = bitten.util.testrunner:unittest'
        ],
    }
)
