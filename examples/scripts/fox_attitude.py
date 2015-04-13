#!/usr/bin/python
# -*- coding: utf-8 -*-
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

# pylint:disable= I0011, E1101, R0912, R0913, R0914, R0915
# E1101 no-member false positif

"""
Fox IMU attitude computation
"""
import sys
import os
import argparse
import numpy as np
import sensbiotk.calib.calib as calib
from sensbiotk.algorithms import martin_ahrs
from sensbiotk.algorithms.basic import find_static_periods
from sensbiotk.io.iofox import load_foxcsvfile
from sensbiotk.io.ahrs import save_ahrs_csvfile
from sensbiotk.transforms3d import quaternions as nq
from sensbiotk.transforms3d.eulerangles import quat2euler

import matplotlib.pyplot as plt

DEF_CALIBFILE = "calib_imu.txt"


def plot_quat(title, timu, quatw, quatx, quaty, quatz):
    """ Plot quaternion
    """
    plt.figure()
    plt.title(title+" Quaternion")
    plt.plot(timu, quatw)
    plt.plot(timu, quatx)
    plt.plot(timu, quaty)
    plt.plot(timu, quatz)
    plt.legend(('qw', 'qx', 'qy', 'qz'))
    return


def plot_euler(title, time, phi, theta, psi):
    """ Plot euler angles
    """
    plt.figure()
    plt.title(title+" Euler angles")
    plt.plot(time, phi*180/np.pi)
    plt.plot(time, theta*180/np.pi)
    plt.plot(time, psi*180/np.pi)
    plt.legend(('e_x', 'e_y', 'e_z'))
    return


def normalize_data(data, param_calib):
    """ normalize_data
    """
    scale = param_calib[1:4, :]
    bias = param_calib[0, :]
    data_n = np.transpose(np.dot(scale,
                                 np.transpose((data-np.transpose(bias)))))
    return data_n


def compute_attitude(datafile, calibfile, anglefile, plotting=True):
    """ compute attitude IMU sensor
    """
    # Load calibration parameters
    [params_acc, params_mag, params_gyr] = calib.load_param(calibfile)
    # Load the recording data
    [time_sens, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz] = \
        load_foxcsvfile(datafile)
    # Find motionless begin periods
    freqs = 200
    start, end = find_static_periods(gyrz, 2 * np.pi/180, 3*freqs)
    static_duration = time_sens[end[0]] - time_sens[start[0]]
    if static_duration < 5.0:
        print "Warning: static duration too low"

    time_imu = time_sens
    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([magx, magy, magz])
    gyr_imu = np.column_stack([gyrx, gyry, gyrz])
    # Init output
    quat = np.zeros((len(acc_imu), 4))
    euler = np.zeros((len(acc_imu), 3))
    observer = martin_ahrs.martin_ahrs()
    # Initialization loop
    quat_offset = [1, 0, 0, 0]
    for i in range(0, end[0]):
        # Applies the Scale and Offset to data
        acc_imu[i, :] = normalize_data(acc_imu[i, :], params_acc)
        mag_imu[i, :] = normalize_data(mag_imu[i, :], params_mag)
        gyr_imu[i, :] = normalize_data(gyr_imu[i, :], params_gyr)
        # Filter call
        if i == 0:
            quat[0] = observer.init_observer(np.hstack([acc_imu[0, :],
                                                        mag_imu[0, :],
                                                        gyr_imu[0, :]]))
        else:
            quat[i] = observer.update(np.hstack([acc_imu[i, :],
                                                 mag_imu[i, :],
                                                 gyr_imu[i, :]]), 0.005)
    quat_offset = nq.conjugate(quat[end-1][0])
    print "Quaternion init", quat_offset

    # Computation loop
    for i in range(end[0], len(acc_imu)):
        # Applies the Scale and Offset to data
        acc_imu[i, :] = normalize_data(acc_imu[i, :], params_acc)
        mag_imu[i, :] = normalize_data(mag_imu[i, :], params_mag)
        gyr_imu[i, :] = normalize_data(gyr_imu[i, :], params_gyr)
        # Filter call
        quat[i] = observer.update(np.hstack([acc_imu[i, :],
                                             mag_imu[i, :],
                                             gyr_imu[i, :]]), 0.005)
        quat[i] = nq.mult(quat_offset, quat[i])
        euler[i] = quat2euler(quat[i])

    # Plot results
    if plotting is True:
        plot_quat("Expe Prima ", time_imu,
                  quat[:, 0], quat[:, 1], quat[:, 2], quat[:, 3])
        plot_euler("Expe Prima ", time_imu,
                   euler[:, 2], euler[:, 1], euler[:, 0])
    # Save results
    save_ahrs_csvfile(anglefile, time_imu, quat, euler)


def launch():
    """ Launch the process taking into account arguments
    """
    # create parser
    parser = argparse.ArgumentParser(
        description="Fox IMU Attitude Computation")
    # add arguments
    parser.add_argument('input', metavar='fox_imu_data.csv',
                        type=str, nargs=1,
                        help="IMU sensors values to be computed")
    parser.add_argument('-o', '--output', type=str,
                        help="Fox IMU attitude values (quaternion/euler)")
    parser.add_argument('-c', '--calib', type=str,
                        help="Fox IMU calibration parameters file")
    parser.add_argument('-p', '--plot', action="store_true",
                        help="Fox IMU calibration parameters file")
    args = parser.parse_args()
    # Arguments verification
    if len(args.input) != 1:
        parser.print_help()
        sys.exit()
    inputfile = args.input[0]
    if args.calib is None:
        args.calib = DEF_CALIBFILE
    calibfile = args.calib
    if args.output is None:
        args.output = os.path.splitext(inputfile)[0]\
            + "_angle" \
            + os.path.splitext(inputfile)[1]
    outputfile = args.output

    # Launch the process
    compute_attitude(inputfile, calibfile, outputfile, args.plot)

    return

if __name__ == '__main__':
    launch()
    plt.show()
