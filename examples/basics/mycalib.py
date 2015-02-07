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
Tests Unit for algorithms/calib
"""

# pylint:disable= I0011, E1101, E0611, C0103
# E1101 no-member false positif
# E0611 no-name false positif
# C0103 Invalid variable name
# W0611 Unused import Axes3D

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

DPATH = "../../sensbiotk/tests/data/"
CALIB_FILE = DPATH + "calib_accelerometer/IMU4/HKB0_02.csv"
#CALIB_FILE = DPATH + "3D_validation/CALIB_ACCEL_MAGNETO/4_IMU4_WAND.csv"


def test_calib_acc():
    """ Test calib_acc function
    """

    from sensbiotk.algorithms.basic import find_static_periods
    from sensbiotk.io.iofox import load_foxcsvfile
    import sensbiotk.calib.calib_acc as calib_acc

    # Load the recording with motionless periods
    [_, accx, accy, accz, _, _, _, _, _, gyrz] = \
        load_foxcsvfile(CALIB_FILE)
    freqs = 200
    # Detects the motionless periods
    start, end = find_static_periods(gyrz, 2 * np.pi/180, 3*freqs)

    acc_stat_x = []
    acc_stat_y = []
    acc_stat_z = []

    for i in range(0, len(start)):
        acc_stat_x = np.concatenate((np.array(acc_stat_x),
                                     accx[range(start[i], end[i])]))
        acc_stat_y = np.concatenate((np.array(acc_stat_y),
                                     accy[range(start[i], end[i])]))
        acc_stat_z = np.concatenate((np.array(acc_stat_z),
                                     accz[range(start[i], end[i])]))

    acc_stat = np.column_stack((acc_stat_x, acc_stat_y, acc_stat_z))
    # Compute the offset and scale
    offset, scale = calib_acc.compute(acc_stat)

    print "OFFSET", offset
    print "SCALE", scale

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

    acc_norm = np.sqrt(np.sum(acc_imu[range(start[0], end[0]), i]**2
                              for i in range(0, 3)))
    m_1 = np.mean(acc_norm)
    s_1 = np.std(acc_norm)
    print "norm_acc", g_after_calib, m_1, s_1

    plt.plot(acc_norm)

    if g_after_calib < 9.91 and g_after_calib > 9.71:
        print "CALIB OK"
    else:
        print "CALIB KO"

    #yield assert_equal, resp, True
    return


def test_calib_mag():
    """ Test calib_mag function
    """
    from sensbiotk.io.iofox import load_foxcsvfile
    import sensbiotk.calib.calib_mag as calib_mag

    # Load the recording
    [_,  _, _, _, m_x, m_y, m_z, _, _, _, ] =\
        load_foxcsvfile(CALIB_FILE)

    data = np.column_stack((m_x, m_y, m_z))
    offset, scale = calib_mag.compute(data)

    print "OFFSET", offset
    print "SCALE", scale

    # Applies the offset and scale to the data
    for i in range(0, len(data)):
        data[i, :] = np.transpose(
            np.dot(scale,
                   np.transpose((data[i, :] - np.transpose(offset)))))

    # Plot signals before values calibration
    plot_calib(m_x, m_y, m_z, "Raw mag.")

    # Plot signals after calibration
    norm_mag_after_calib = plot_calib(data[:, 0],
                                      data[:, 1], data[:, 2], "Calib mag.")

    # It has to be close to 1.0 if the computed parameters are satisfying.
    if norm_mag_after_calib < 1.2 and norm_mag_after_calib > 0.8:
        print "CALIB OK"
    else:
        print "CALIB KO"
    return


def plot_calib(sensx, sensy, sensz, mytitle):
    """ calibration plot debugging
    """
    # Norm of the 3D signal
    cnorm = np.sqrt(sensx**2 + sensy**2 + sensz**2)

    # Signal plot of the 3 axis
    # and the norm
    plt.figure()
    plt.title(mytitle)
    plt.plot(sensx)
    plt.plot(sensy)
    plt.plot(sensz)
    plt.plot(cnorm)
    # Data 3D plot
    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    axes.set_title(mytitle)
    axes.scatter(sensx, sensy, sensz)
    # 3D reference sphere plot
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    axes.plot_wireframe(x, y, z, color="r")

    mean_cnorm = np.mean(cnorm)
    print "Norm", mytitle, mean_cnorm, np.std(cnorm)

    return mean_cnorm


if __name__ == '__main__':
    test_calib_mag()
    #test_calib_acc()
    plt.show()
