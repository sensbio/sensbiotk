# -*- coding: utf-8 -*-
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
TEST MADGWICK AHRS
"""

import numpy as np
from nose.tools import assert_equal
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib as calib
import sensbiotk.algorithms.mahony_ahrs as madgwick
import scipy.io as sio

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

def test_madgwick_ahrs():

    quat_dict = sio.loadmat('data/test_madgwick_ahrs/quaternion_madgwick.mat')
    quat_verif = quat_dict['quaternion']

    [params_acc, params_mag, params_gyr] = \
        calib.load_param("data/test_madgwick_ahrs/CalibrationFileIMU6.txt")

    # Load the recording data
    [_, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
        load_foxcsvfile("data/test_madgwick_ahrs/1_IMU6_RIGHT_FOOT.csv")

    # Applies the Scale and Offset to data
    scale_acc = params_acc[1:4, :]
    bias_acc = params_acc[0, :]
    scale_mag = params_mag[1:4, :]
    bias_mag = params_mag[0, :]
    scale_gyr = params_gyr[1:4, :]
    bias_gyr = params_gyr[0, :]

    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([mx, my, mz])
    gyr_imu = np.column_stack([gyrx, gyry, gyrz])

    quaternion = np.zeros((len(acc_imu), 4))

    quaternion[0, :] = [1, 0, 0, 0]

    for i in range(0, len(acc_imu)-1):
        acc_imu[i, :] = np.transpose(np.dot(
        scale_acc, np.transpose((acc_imu[i, :]-np.transpose(bias_acc)))))
        mag_imu[i, :] = np.transpose(np.dot(
        scale_mag, np.transpose((mag_imu[i, :]-np.transpose(bias_mag)))))
        gyr_imu[i, :] = np.transpose(np.dot(
        scale_gyr, np.transpose((gyr_imu[i, :]-np.transpose(bias_gyr)))))
        quaternion[i+1] = madgwick.update(
        quaternion[i], np.hstack([acc_imu[i, :], mag_imu[i, :], gyr_imu[i, :]]))

    yield assert_equal, quaternion.all() == quat_verif.all(), "OK"

if __name__ == '__main__':
    test_madgwick_ahrs()
