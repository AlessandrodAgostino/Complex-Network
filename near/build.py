#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

__package__ = "build_near"

__author__  = ["Alessandro d'Agostino",
               'Mattia Ceccarelli',
               'Riccardo Scheda']

__email__ = ['alessadrdagostino@studio.unibo.it',
             'mattia.ceccarelli3@studio.unibo.it',
             'riccardo.scheda@studio.unibo.it']

def get_requires (requirements_filename):
  """
  What packages are required for this module to be executed?
  """
  with open(requirements_filename, 'r') as fp:
    requirements = fp.read()

  return list(filter(lambda x: x != '', requirements.split()))

def read_description (readme_filename):
  """
  Description package from filename
  """

  try:

    with open(readme_filename, 'r') as fp:
      description = '\n'
      description += fp.read()

  except Exception:
    return ''
