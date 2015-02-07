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
Tests Unit for sensbiotk/calib
"""

# pylint:disable= I0011, E1101, E0611
# E1101 no-member false positif
# E0611 no-name false positif

import numpy as np
from nose.tools import assert_equal


def test_calib_acc():
    """ Test calib_acc function
    """

    from sensbiotk.algorithms.basic import find_static_periods_3D
    from sensbiotk.io.iofox import load_foxcsvfile
    import sensbiotk.calib.calib_acc as calib_acc

    # Load the recording with motionless periods
    [_, accx, accy, accz, _, _, _, gyrx, gyry, gyrz] = \
        load_foxcsvfile("data/calib_accelerometer/IMU4/HKB0_02.csv")
    freqs = 200
    # Detects the motionless periods
    start, end = find_static_periods_3D(np.column_stack((gyrx, gyry, gyrz)), 4 * np.pi/180, 2*freqs)

    acc_stat_x = []
    acc_stat_y = []
    acc_stat_z = []

    for i in range(0, len(start)):
        acc_stat_x = np.concatenate((np.array(acc_stat_x),
                                     accx[start[i]:end[i]+1]))
        acc_stat_y = np.concatenate((np.array(acc_stat_y),
                                     accy[start[i]:end[i]+1]))
        acc_stat_z = np.concatenate((np.array(acc_stat_z),
                                     accz[start[i]:end[i]+1]))

    acc_stat = np.column_stack((acc_stat_x, acc_stat_y, acc_stat_z))
    # Compute the offset and scale
    offset, scale = calib_acc.compute(acc_stat)

    acc_imu = np.transpose(np.vstack((np.transpose(accx),
                                      np.transpose(accy), np.transpose(accz))))

    # if the IMU is well calibrated, the norm's acceleration is equal
    # to 9.81 along a motionless period
    #g_before_calib = np.sqrt(np.mean(acc_imu[range(start[0], end[0]), 0])**2
    #                       + np.mean(acc_imu[range(start[0], end[0]), 1])**2
    #                       + np.mean(acc_imu[range(start[0], end[0]), 2])**2)

    # Applies the offset and scale to the data
    for i in range(0, len(acc_imu)):
        acc_imu[i, :] = np.transpose(
            np.dot(scale,
                   np.transpose((acc_imu[i, :] - np.transpose(offset)))))

    # Computes the norm on the motionless periods.
    # It has to be close to 9.81 if the computed parameters are satisfying.
    g_after_calib = np.sqrt(np.mean(acc_imu[range(start[0], end[0]), 0])**2
                            + np.mean(acc_imu[range(start[0], end[0]), 1])**2
                            + np.mean(acc_imu[range(start[0], end[0]), 2])**2)
    print g_after_calib

    if g_after_calib < 9.91 and g_after_calib > 9.71:
        resp = True
    else:
        resp = False

    yield assert_equal, resp, True


def test_calib_mag():
    """ Test calib_mag function
    """
    from sensbiotk.io.iofox import load_foxcsvfile
    import sensbiotk.calib.calib_mag as calib_mag

    # Load the recording
    [_, _, _, _, m_x, m_y, m_z, _, _, _, ] =\
        load_foxcsvfile("data/calib_accelerometer/IMU4/HKB0_02.csv")
    data = np.column_stack((m_x, m_y, m_z))
    offset, scale = calib_mag.compute(data)

    # Applies the offset and scale to the data
    for i in range(0, len(data)):
        data[i, :] = np.transpose(
            np.dot(scale,
                   np.transpose((data[i, :] - np.transpose(offset)))))

    # Computes the norm on 3D signals.
    norm_mag_after_calib = np.mean(np.sqrt(data[:, 0]**2 +
                                           data[:, 1]**2 +
                                           data[:, 2]**2))

    # It has to be close to 1.0 if the computed parameters are satisfying.
    if norm_mag_after_calib < 1.2 and norm_mag_after_calib > 0.8:
        resp = True
    else:
        resp = False

    yield assert_equal, resp, True
