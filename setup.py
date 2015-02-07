#!/usr/bin/env python

# -*- coding: utf-8; -*-
# This file is a part of sensbiotk
# Contact : sensbio@inria.fr
# Copyright (C) 2014  INRIA (Contact: sensbiotk@inria.fr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#from distutils.core import setup
import sys

# Package description
CLASSIFIERS = """\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Science/Research
Programming Language :: Python :: 2.7
Topic :: Software Development
"""

LONG_DESCRIPTION = \
"""
=========
SENSBIOTK
=========

Senbiotk toolbox for Python.

The aim of SensbioTK is to produce a platform-independent Python environment for the acquisition, analysis and visualization of motion capture

"""

NAME                = 'SensbioTk'
DESCRIPTION         = "Senbiotk toolbox for Python for acquisition, analysis and visualization of motion capture"
URL                 = "http://sensas.gforge.inria.fr/wiki/doku.php?id=sensbio"
AUTHOR              = "Roger Pissard-Gibollet and al."
AUTHOR_EMAIL        = "sensbio@inria.fr"
PLATFORMS           = [ "Linux"]
MAJOR               = 2
MINOR               = 0
MICRO               = 0
ISRELEASED          = False
LICENCE             = "GNU GPL v3"
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None,parent_package,top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)
    # The quiet=True option will silence all of the name setting warnings
    config.add_subpackage('sensbiotk', 'sensbiotk')
    config.make_config_py() 
    return config

# Module dependency checking
#package_check('numpy', INFO_VARS['NUMPY_MIN_VERSION'])
#package_check('scipy', INFO_VARS['SCIPY_MIN_VERSION'])

def setup_package():
    
    from numpy.distutils.core import setup

    setup(name = NAME,
          license = LICENCE,
          version = VERSION,
          description = DESCRIPTION,         
          long_description = LONG_DESCRIPTION,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          url = URL,
          classifiers = CLASSIFIERS,
          platforms=PLATFORMS,
          configuration=configuration
          )


if __name__ == "__main__":
    setup_package()
