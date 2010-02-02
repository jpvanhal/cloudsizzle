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
    description = 'Social study plan9er for Aalto University students',
    install_requires = [
        'Django >= 1.1',
        'Scrapy == 0.8',
        'kpwrapper >= 1.0.0',
        'asi >= 0.9',
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
