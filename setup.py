# coding=utf-8
# Not importing unicode_literals because in Python 2 distutils, some
# values are expected to be byte strings.
from __future__ import absolute_import, division, print_function

from codecs import StreamReader, open
from os.path import dirname, join, realpath

from setuptools import setup

cwd = dirname(realpath(__file__))

##
# Load long description for PyPi.
with open(join(cwd, 'README.rst'), 'r', 'utf-8') as f: # type: StreamReader
    long_description = f.read()


##
# Off we go!
setup(
    name = 'data-providers',
    description = 'Generic implementation of the flywheel design pattern.',
    url = 'https://data-providers.readthedocs.io/',

    version = '2.0.0',

    packages = ['data_providers'],

    long_description = long_description,

    install_requires = [
        'six',
        'typing; python_version < "3.0"',
    ],

    test_suite    = 'test',
    test_loader   = 'nose.loader:TestLoader',
    tests_require = ['nose'],

    license = 'MIT',

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords = 'flywheel pattern',

    author          = 'Phoenix Zerin',
    author_email    = 'phoenix.zerin@eflglobal.com',
)
