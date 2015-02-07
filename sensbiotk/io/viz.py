# -*- coding: utf-8; -*-
# This file is a part of sensbiotk
# Contact : sensbiotk@inria.fr
# Copyright (C) 2015  INRIA
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
Plot for sensors data
"""

# pylint:disable= I0011, E1101, R0913
# E1101 no-member false positif

import matplotlib.pyplot as plt

def plot_imu(num, title, time, acc, mag, gyr):
    """
    Plot IMU datas

    @param id   : plot number, negative for automatic numbering
    @param title: title of the plot
    @param time :
    @param acc  :
    @param mag  :
    @param gyr  :

    @return: none
    """

    if num < 0:
        plt.figure()
    else:
        plt.figure(num)

    ax1 = plt.subplot(311)
    plt.plot(time, acc[:, 0:3])
    plt.title(title)
    plt.legend(('x', 'y', 'z'), bbox_to_anchor=(0, 1, 1, 0),
              ncol=2, loc=3, borderaxespad=0.)
    plt.ylabel('ACC (m/s^2)')
    plt.subplot(312, sharex=ax1)
    plt.plot(time, mag[:, 0:3])
    plt.ylabel('MAG (gauss)')
    plt.subplot(313, sharex=ax1)
    plt.plot(time, gyr[:, 0:3])
    plt.ylabel('GYR (rad/s)')
    plt.xlabel('time (s)')

    return


def plot_show():
    """
    plt.show()
    """
    plt.show()
    return


def test1():
    """
    Test  plot_imu

    @param : none

    @return: OK/ERROR
    """
    import sensbiotk.io.iofox_deprec as iofox

    [time, acc, mag, gyr] = \
        iofox.load_foximu_csvfile("../tests/data/output_imu.csv")

    plot_imu(1, "FOX IMU", time[:, 1], acc, mag, gyr)

    #[time, acc, mag, gyr] = fox.load_foximu_csvfile("imuf.txt")
    #plot_imu(2, "FOX IMU", time[:, 1], acc, mag, gyr)

    return


def test2():
    """
    Test  samples time

    @param : none

    @return: OK/ERROR
    """
    import numpy as np
    import sensbiotk.io.iofox_deprec as iofox

    [time, _, _, _] = \
        iofox.load_foximu_csvfile("../tests/data/output_imu.csv")

    plt.figure(2)
    plt.title("FOX IMU samples verification")
    plt.plot(time[1:, 1], time[1:, 2])

    print "DT Min (ms) =", np.min(time[1:, 2])*1000, "DT Max (ms) =",\
        np.max(time[1:, 2]) * 1000
    print "DT Mean(ms) =", np.mean(time[1:, 2])*1000, "DT Std (ms) =",\
        np.std(time[1:, 2]) * 1000

    plt.show()

    return "OK"


def test3():
    """
    Test  plot_imu

    @param : none

    @return: OK/ERROR
    """
    import sensbiotk.io.iofox as iofox

    [time, acc, mag, gyr] = iofox.load_foximu_csvfile(
        "../tests/data/HKB1_01_acc.csv", "../tests/data/HKB1_01_mag.csv",
        "../tests/data/HKB1_01_gyr.csv", 0.06)
    plot_imu(1, "FOX IMU", time, acc, mag, gyr)

    return


if __name__ == '__main__':
    print "TEST 1"
    test1()
    print "TEST 2"
    test2()
    print "TEST 3"
    test3()

    plt.show()
