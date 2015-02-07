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
Tests Unit for iofox module
"""

import numpy as np
import filecmp
from sensbiotk.io import iofox_deprec as fox

from nose.tools import assert_equal

# pylint:disable= I0011, E1101
# E1101 no-member false positif


def test_load():
    """ Test loading files
    """

    # read and convert HIGPS01.RAW with convert_fox_rawfile
    resp = fox.convert_fox_rawfile("data/imutest_deprec.raw",
                                   "tmpdata/imutest_deprec_imu.csv",
                                   "tmpdata/imutest_deprec_presst.csv")
    yield assert_equal, resp, "OK"

    resp = filecmp.cmp("tmpdata/imutest_deprec_imu.csv", "data/imutest_deprec_imu.csv")
    yield assert_equal, resp, True
    resp = filecmp.cmp("tmpdata/imutest_deprec_presst.csv", "data/imutest_deprec_presst.csv")
    yield assert_equal, resp, True

    # read data/output_imu.csv with load_foximu_csvfile
    [time, acc, mag, gyr] = \
        fox.load_foximu_csvfile("data/imutest_deprec_imu.csv")
    sizedata = 1764
    if (np.size(time) == sizedata) and (np.size(acc) == sizedata)\
            and (np.size(mag) == sizedata) and (np.size(gyr) == sizedata):
        sot = 1
    else:
        sot = 0
    yield assert_equal, sot, 1

    # read data/output_presst.csv with load_foxpresst_csvfile
    [time, press, temp] = \
        fox.load_foxpresst_csvfile("data/imutest_deprec_presst.csv")
    if ((np.size(time) == sizedata) and (np.size(press) == sizedata/3) and
       (np.size(temp) == sizedata/3)):
        sot = 1
    else:
        sot = 0
    yield assert_equal, sot, 1
