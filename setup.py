#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os

try:
  from setuptools import setup
  from setuptools import find_packages

except ImportError:
  from distutils.core import setup
  from distutils.core import find_packages


from NumPyNet.build import get_requires
from NumPyNet.build import read_description

here = os.path.abspath(os.path.dirname(__file__))

# Package data
NAME = 'near'
DESCRIPTION = 'NEtwork analysis in ARangoDB'
URL = 'https://github.com/AlessandrodAgostino/Complex-Network'
EMAIL = ['alessadrdagostino@studio.unibo.it', 'mattia.ceccarelli3@studio.unibo.it', 'riccardo.scheda@studio.unibo.it']
AUTHOR = ["Alessandro d'Agostino", 'Mattia Ceccarelli', 'Riccardo Scheda']
REQUIRES_PYTHON = '>=3.7'
VERSION = '0.1'
KEYWORDS = 'complex-networks net data-science arangodb data-analysis'

README_FILENAME = os.path.join(here, 'README.md')
REQUIREMENTS_FILENAME = os.path.join(here, 'requirements.txt')
VERSION_FILENAME = os.path.join(here, 'near', '__version__.py')

setup(
  name                          = NAME,
  version                       = VERSION,
  description                   = DESCRIPTION,
  long_description              = README_FILENAME,
  long_description_content_type = 'text/markdown',
  author                        = AUTHOR,
  author_email                  = EMAIL,
  maintainer                    = AUTHOR,
  maintainer_email              = EMAIL,
  python_requires               = REQUIRES_PYTHON,
  install_requires              = get_requires(REQUIREMENTS_FILENAME),
  url                           = URL,
  download_url                  = URL,
  keywords                      = KEYWORDS,
  packages                      = find_packages(include=['', ''], exclude=('test', 'testing')),
  #include_package_data          = True, # no absolute paths are allowed
  platforms                     = 'Linux',
  # classifiers                   =[
  #                                  #'License :: OSI Approved :: GPL License',
  #                                  'Programming Language :: Python',
  #                                  'Programming Language :: Python :: 3',
  #                                  'Programming Language :: Python :: 3.7',
  #                                  'Programming Language :: Python :: Implementation :: CPython',
  #                                  'Programming Language :: Python :: Implementation :: PyPy'
  #                                ],
  # license                       = 'MIT'
)
