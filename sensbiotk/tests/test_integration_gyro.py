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
Tests Unit for sensbiotk/algorithms/integration_gyro
"""
import numpy as np
import sensbiotk.algorithms.integration_gyro as integration_gyro
from sensbiotk.io.iofox import load_foxcsvfile


def test_integration_gyro_3D():
    [time_imu, _, _, _, _, _, _, gyrx, gyry, gyrz] = \
        load_foxcsvfile("data/3D_validation/3/3_IMU4_WAND.csv")
    freqs = 200
    data_vicon = np.loadtxt("data/3D_validation/2/GLOBAL_EULER_XYZ.txt",skiprows=2)
    time_vicon = data_vicon[:,0]
    theta_x_vicon = data_vicon[:,1]*180/np.pi+177
    theta_y_vicon = data_vicon[:,2]*180/np.pi
    theta_z_vicon = data_vicon[:,3]*180/np.pi

    #Remove wrong values from Vicon data
    theta_x_vicon[np.abs(theta_x_vicon) > 130] = 0   
    theta_y_vicon[np.abs(theta_y_vicon) > 130] = 0   
    theta_z_vicon[np.abs(theta_z_vicon) > 130] = 0  
#    theta_x_vicon[3130:3630] = theta_x_vicon[3129]  
#    theta_y_vicon[3130:3630] = theta_y_vicon[3129]  
#    theta_z_vicon[3130:3630] = theta_z_vicon[3129]  
    

    plot(time_vicon, theta_x_vicon)
    plot(time_vicon, theta_y_vicon)
    plot(time_vicon, theta_z_vicon)
    
    
    theta_x_imu = integration_gyro.compute(gyrx)
    theta_y_imu = integration_gyro.compute(gyry)
    theta_z_imu = integration_gyro.compute(gyrz)

    plot(time_imu, theta_x_imu)
    plot(time_imu, theta_y_imu,)
    plot(time_imu, theta_z_imu)
    legend(('x_vicon','y_vicon','z_vicon','x_imu','y_imu','z_imu'))
    
    
if __name__ == '__main__':
   test_integration_gyro_3D()   
