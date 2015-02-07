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

# pylint:disable= I0011, E1101, E0611
# E1101 no-member false positif
# E0611 no-name false positif

import numpy as np
import filecmp
from sensbiotk.io import iofox as fox
from numpy.testing import assert_array_almost_equal

from nose.tools import assert_equal


def test_convert():
    """ Test convert_sensors_rawfile function
    """
    # conversion of imutest
    resp = fox.convert_sensors_rawfile("data/imutest.raw",
                                       "tmpdata/imutest_acc.csv",
                                       "tmpdata/imutest_mag.csv",
                                       "tmpdata/imutest_gyr.csv")
    yield assert_equal, resp, "OK"

    resp = filecmp.cmp("tmpdata/imutest_acc.csv", "data/imutest_acc.csv")
    yield assert_equal, resp, True
    resp = filecmp.cmp("tmpdata/imutest_mag.csv", "data/imutest_mag.csv")
    yield assert_equal, resp, True
    resp = filecmp.cmp("tmpdata/imutest_gyr.csv", "data/imutest_gyr.csv")
    yield assert_equal, resp, True

    # conversion of doortest_big  (a big file)
    resp = fox.convert_sensors_rawfile("data/doortest_big.raw",
                                       "tmpdata/doortest_big_acc.csv",
                                       "tmpdata/doortest_big_mag.csv",
                                       "tmpdata/doortest_big_gyr.csv")
    yield assert_equal, resp, "OK"

    resp = filecmp.cmp("tmpdata/doortest_big_acc.csv",
                       "data/doortest_big_acc.csv")
    yield assert_equal, resp, True
    resp = filecmp.cmp("tmpdata/doortest_big_mag.csv",
                       "data/doortest_big_mag.csv")
    yield assert_equal, resp, True
    resp = filecmp.cmp("tmpdata/doortest_big_gyr.csv",
                       "data/doortest_big_gyr.csv")
    yield assert_equal, resp, True

    # conversion of gpiotest
    resp = fox.convert_sensors_rawfile("data/gpiotest.raw",
                                       "tmpdata/gpiotest_acc.csv",
                                       "tmpdata/gpiotest_mag.csv",
                                       "tmpdata/gpiotest_gyr.csv",
                                       "tmpdata/gpiotest_presst.csv",
                                       "tmpdata/gpiotest_gpio.csv")
    yield assert_equal, resp, "OK"
    resp = filecmp.cmp("tmpdata/gpiotest_gpio.csv",
                       "data/gpiotest_gpio.csv")
    yield assert_equal, resp, True


def test_load():
    """ Test loading functions
    """

    # read imutest_acc/mag/gyr with load_foximu_csvfile
    [time, acc, mag, gyr] = fox.load_foximu_csvfile(
        "data/imutest_acc.csv",
        "data/imutest_mag.csv",
        "data/imutest_gyr.csv",
        0.06, 1)

    sizedata = 285

    if ((np.size(time) == sizedata) and (np.size(acc) == sizedata*3) and
       (np.size(mag) == sizedata*3) and (np.size(gyr) == sizedata*3)):
        resp = True
    else:
        resp = False

    yield assert_equal, resp, True

    # read doortest_big_acc with load_foxacc_csvfile
    [timea, acc] = fox.load_foxacc_csvfile("data/doortest_big_acc.csv")
    sizedata = 262628
    if (np.size(timea[:, 0]) == sizedata) and (np.size(acc) == sizedata*3):
        resp = True
    else:
        resp = False
    yield assert_equal, resp, True

    # read doortest_big_mag with load_foxmag_csvfile
    [timem, mag] = fox.load_foxmag_csvfile("data/doortest_big_mag.csv")
    sizedata = 392876
    if (np.size(timem[:, 0]) == sizedata) and (np.size(mag) == sizedata*3):
        resp = True
    else:
        resp = False
    yield assert_equal, resp, True

    # read doortest_big_gyr with load_foxgyr_csvfile
    [timeg, gyr] = fox.load_foxgyr_csvfile("data/doortest_big_gyr.csv")
    sizedata = 270388
    if (np.size(timeg[:, 0]) == sizedata) and (np.size(gyr) == sizedata*3):
        resp = True
    else:
        resp = False
    yield assert_equal, resp, True

    # read gpiotest with load_foxgpio_csvfile
    [timeio, gpio] = fox.load_foxgpio_csvfile("data/gpiotest_gpio.csv")
    sizedata = 7143
    if (np.size(timeio[:, 0]) == sizedata) and (np.size(gpio) == sizedata*5):
        resp = True
    else:
        resp = False
    yield assert_equal, resp, True


def test_save():
    """ Test saving functions
    """

    # save imutest_acc with load_foxacc_csvfile
    [time, acc] = fox.load_foxacc_csvfile("data/imutest_acc.csv")
    resp = fox.save_foxacc_csvfile("tmpdata/imutest_acc_save.csv", time, acc)
    yield assert_equal, resp, "OK"

    [time1, acc1] = fox.load_foxacc_csvfile("tmpdata/imutest_acc_save.csv")
    yield assert_array_almost_equal, time, time1
    yield assert_array_almost_equal, acc, acc1

    # save imutest_mag with load_foxmag_csvfile
    [time, mag] = fox.load_foxmag_csvfile("data/imutest_mag.csv")
    resp = fox.save_foxmag_csvfile("tmpdata/imutest_mag_save.csv", time, mag)
    yield assert_equal, resp, "OK"

    [time1, mag1] = fox.load_foxmag_csvfile("tmpdata/imutest_mag_save.csv")
    yield assert_array_almost_equal, time, time1
    yield assert_array_almost_equal, mag, mag1

    # save imutest_gyr with load_foxgyr_csvfile
    [time, gyr] = fox.load_foxgyr_csvfile("data/imutest_gyr.csv")
    resp = fox.save_foxgyr_csvfile("tmpdata/imutest_gyr_save.csv", time, gyr)
    yield assert_equal, resp, "OK"

    [time1, gyr1] = fox.load_foxgyr_csvfile("tmpdata/imutest_gyr_save.csv")
    yield assert_array_almost_equal, time, time1
    yield assert_array_almost_equal, gyr, gyr1

    #  save_foxsignals_csvfile
    [time, acc, mag, gyr] = fox.load_foximu_csvfile(
        "data/imutest_acc.csv",
        "data/imutest_mag.csv",
        "data/imutest_gyr.csv",
        0.06, 1)

    resp = fox.save_foxsignals_csvfile(time, acc, mag, gyr,
                                       "tmpdata/imutest.csv")
    yield assert_equal, resp, "OK"

    # TBD test if data are ok.
    # data = fox.load_foxcsvfile("tmpdata/imutest.csv")
