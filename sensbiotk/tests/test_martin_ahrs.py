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
TEST MARTIN SALAUN AHRS
"""

import numpy as np
from nose.tools import assert_equal
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib as calib
import sensbiotk.algorithms.martin_ahrs as martin
import sensbiotk.transforms3d.quaternions as nq

import scipy.io as sio

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

def test_martin_ahrs():

    quat_dict = sio.loadmat('data/test_martin_ahrs/quaternion_martin.mat')
    quat_verif = quat_dict['quaternion']

    [_, params_mag, params_gyr] = \
        calib.load_param("data/test_martin_ahrs/CalibrationFileIMU6.txt")

    # Load the recording data
    [_, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
        load_foxcsvfile("data/test_martin_ahrs/1_IMU6_RIGHT_FOOT.csv")

    # Applies the Scale and Offset to data
    scale_mag = params_mag[1:4, :]
    bias_mag = params_mag[0, :]
    scale_gyr = params_gyr[1:4, :]
    bias_gyr = params_gyr[0, :]

    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([mx, my, mz])
    gyr_imu = np.column_stack([gyrx, gyry, gyrz])

    observer = martin.martin_ahrs()

    quaternion = np.zeros((len(acc_imu), 4))
    quaternion_corr = np.zeros((len(acc_imu), 4))

    data_init = np.mean(np.hstack(
    [acc_imu[0:200, :], \
    mag_imu[0:200, :], \
    gyr_imu[0:200, :]]), 0) # mean of the first static 2 seconds

    quaternion[0, :] = observer.init_observer(data_init)

    for i in range(1, len(acc_imu)-1):
        mag_imu[i, :] = np.transpose(np.dot(
        scale_mag, np.transpose((mag_imu[i, :]-np.transpose(bias_mag)))))
        gyr_imu[i, :] = np.transpose(np.dot(
        scale_gyr, np.transpose((gyr_imu[i, :]-np.transpose(bias_gyr)))))
        quaternion[i+1] = observer.update(
        np.hstack([acc_imu[i, :], mag_imu[i, :], gyr_imu[i, :]]), 0.005)

    conj_q_init = nq.conjugate(quaternion[150, :])
    for i in range(1, len(acc_imu)-1):
        quaternion_corr[i+1] = nq.mult(conj_q_init, quaternion[i+1])


    yield assert_equal, quaternion_corr.all() == quat_verif.all(), "OK"

if __name__ == '__main__':
    test_martin_ahrs()
