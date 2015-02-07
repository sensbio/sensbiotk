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
"""
Tests Unit for io ahrs module
"""

# pylint:disable= I0011, E1101, E0611
# E1101 no-member false positif
# E0611 no-name false positif

import numpy as np
from sensbiotk.io.ahrs import save_ahrs_csvfile
from sensbiotk.io.ahrs import load_ahrs_csvfile
from nose.tools import assert_equal


def test_loadsave():
    """ Test functions load_ahrs_csvfile and save_ahrs_csvfile
    """

    timu, quat, euler = load_ahrs_csvfile("data/output_ahrs.csv")
    save_ahrs_csvfile("tmpdata/output_ahrs_copy.csv", timu, quat, euler)
    timu_copy, quat_copy, euler_copy = \
        load_ahrs_csvfile("tmpdata/output_ahrs_copy.csv")

    timu_cmp = timu - timu_copy
    quat_cmp = quat - quat_copy
    euler_cmp = euler - euler_copy

    yield assert_equal, np.count_nonzero(timu_cmp), 0
    yield assert_equal, np.count_nonzero(quat_cmp), 0
    yield assert_equal, np.count_nonzero(euler_cmp), 0
