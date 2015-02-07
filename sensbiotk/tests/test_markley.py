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
Tests Unit for sensbiotk/algorithms/markley

EN COURS...

"""

import numpy as np
import sensbiotk.algorithms.markley as markley
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib as calib

def test_markley():

    # Compute 
    [params_acc, params_mag, params_gyr] = \
        calib.compute(imuNumber=4 ,filepath="data/3D_validation/CALIB_ACCEL_MAGNETO/4_IMU4_WAND.csv")

    # Load the recording data 
    [time_imu, accx, accy, accz, mx, my, mz, _, _, _] = \
        load_foxcsvfile("data/3D_validation/3/3_IMU4_WAND.csv")

    # Applies the Scale and Offset to data
    scale_acc = params_acc[1:4,:]
    bias_acc = params_acc[0,:]
    scale_mag = params_mag[1:4,:]
    bias_mag = params_mag[0,:]    
    
    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([mx, my, mz])
    
    quaternion = np.zeros((len(acc_imu),4))

    for i in range(0,len(acc_imu)):
        acc_imu[i,:]= np.transpose(np.dot(scale_acc,np.transpose((acc_imu[i,:]-np.transpose(bias_acc)))))
        mag_imu[i,:]= np.transpose(np.dot(scale_mag,np.transpose((mag_imu[i,:]-np.transpose(bias_mag)))))
        quaternion[i]= markley.compute(np.hstack([acc_imu[i,:],mag_imu[i,:]]))

    return quaternion        


#if __name__ == '__main__':
#   test_markley() 


