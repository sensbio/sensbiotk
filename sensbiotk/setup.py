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

import sys


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('sensbiotk',parent_package,top_path)
    config.add_subpackage('io')
    config.add_subpackage('algorithms') 
    config.add_subpackage('calib') 
    config.add_subpackage('driver')
    config.add_subpackage('transforms3d')
    config.add_subpackage('driver')
    config.add_subpackage('calib')
    config.add_subpackage('tests')
    config.make_config_py() 
    return config

  
if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
