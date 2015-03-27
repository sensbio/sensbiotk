## -*- coding: utf-8; -*-
# This file is a part of sensbiotk
# Contact : sensbio@inria.fr
# Copyright (C) 2015  INRIA (Contact: sensbiotk@inria.fr)
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
Computes the two knee angles from a static initial position, with a geometrical and sensor calibration.
Computes the quaternion of the trunk and its respective euler transformation (ZYX) using Martin Salaun algorithm.
Save the outputs in a .mat file.

"""

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

import numpy as np 
import matplotlib.pyplot as plt
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib_geom as calib_geom
import sensbiotk.algorithms.martin_ahrs as martin
import sensbiotk.calib.calib as calib
import sensbiotk.algorithms.goniometer as goniometer
from sensbiotk.transforms3d.eulerangles import quat2euler
import sensbiotk.transforms3d.quaternions as nq
import scipy.io as sio

close('all')
def tug():
    
    trial_number = 8  
    
    calib_sensor_shank_right = 'data/CALIB/9_IMU4_RIGHT_SHANK.csv' #rot
    calib_sensor_thigh_right = 'data/CALIB/9_IMU6_RIGHT_THIGH.csv' #ref
    calib_sensor_shank_left = 'data/CALIB/9_IMU5_LEFT_SHANK.csv' #rot
    calib_sensor_thigh_left = 'data/CALIB/9_IMU9_LEFT_THIGH.csv' #ref
    calib_sensor_trunk = 'data/CALIB/9_IMU8_TRUNK.csv'
    
    trial_file_shank_right = 'data/'+str(trial_number)+'/'+str(trial_number)+'_IMU4_RIGHT_SHANK.csv'
    trial_file_thigh_right = 'data/'+str(trial_number)+'/'+str(trial_number)+'_IMU6_RIGHT_THIGH.csv'
    trial_file_shank_left = 'data/'+str(trial_number)+'/'+str(trial_number)+'_IMU5_LEFT_SHANK.csv'
    trial_file_thigh_left = 'data/'+str(trial_number)+'/'+str(trial_number)+'_IMU9_LEFT_THIGH.csv'
    trial_file_trunk = 'data/'+str(trial_number)+'/'+str(trial_number)+'_IMU8_TRUNK.csv'
    
    ######################################################
    # Sensors (scale/offset) calib parameters computation
    ######################################################
    [_, params_mag_right_thigh, _] = \
           calib.compute(imuNumber=6 ,filepath=calib_sensor_thigh_right, param = 3)
           
    [_, params_mag_right_shank, _] = \
           calib.compute(imuNumber=4 ,filepath=calib_sensor_shank_right, param = 3)
           
    [_, params_mag_left_thigh, _] = \
           calib.compute(imuNumber=9 ,filepath=calib_sensor_thigh_left, param = 3)
           
    [_, params_mag_left_shank, _] = \
           calib.compute(imuNumber=5 ,filepath=calib_sensor_shank_left, param = 3) 
           
    [_, params_mag_trunk, _] = \
           calib.compute(imuNumber=8 ,filepath=calib_sensor_trunk, param = 3) 
       
    scale_mag_right_thigh = params_mag_right_thigh[1:4,:]
    bias_mag_right_thigh = params_mag_right_thigh[0,:]
    
    scale_mag_right_shank = params_mag_right_shank[1:4,:]
    bias_mag_right_shank = params_mag_right_shank[0,:]    
    
    scale_mag_left_thigh = params_mag_left_thigh[1:4,:]
    bias_mag_left_thigh = params_mag_left_thigh[0,:]
    
    scale_mag_left_shank = params_mag_left_shank[1:4,:]
    bias_mag_left_shank = params_mag_left_shank[0,:]    
    
    scale_mag_trunk = params_mag_left_shank[1:4,:]
    bias_mag_trunk = params_mag_left_shank[0,:]        

    ######################################################
    # Load trials data
    ######################################################   
    # right thigh
    [time_imu_right_thigh, accx_right_thigh, accy_right_thigh, accz_right_thigh, \
    mx_right_thigh, my_right_thigh, mz_right_thigh, gyrx_right_thigh, gyry_right_thigh, gyrz_right_thigh] = \
            load_foxcsvfile(trial_file_thigh_right)        
    # left thigh
    [time_imu_left_thigh, accx_left_thigh, accy_left_thigh, accz_left_thigh, \
    mx_left_thigh, my_left_thigh, mz_left_thigh, gyrx_left_thigh, gyry_left_thigh, gyrz_left_thigh] = \
            load_foxcsvfile(trial_file_thigh_left)
    # right shank
    [time_imu_right_shank, accx_right_shank, accy_right_shank, accz_right_shank, \
    mx_right_shank, my_right_shank, mz_right_shank, gyrx_right_shank, gyry_right_shank, gyrz_right_shank] = \
            load_foxcsvfile(trial_file_shank_right)
    # left shank
    [time_imu_left_shank, accx_left_shank, accy_left_shank, accz_left_shank, \
    mx_left_shank, my_left_shank, mz_left_shank, gyrx_left_shank, gyry_left_shank, gyrz_left_shank] = \
            load_foxcsvfile(trial_file_shank_left)
    # trunk
    [time_imu_trunk, accx_trunk, accy_trunk, accz_trunk, \
    mx_trunk, my_trunk, mz_trunk, gyrx_trunk, gyry_trunk, gyrz_trunk] = \
            load_foxcsvfile(trial_file_trunk)
            
            
    ######################################################
    # Applies scale and offset on magnetometer data
    ######################################################

    nb_common_samples = np.amin([len(time_imu_right_thigh), len(time_imu_left_thigh), len(time_imu_right_shank),\
    len(time_imu_left_shank), len(time_imu_trunk)])            
            
    acc_imu_right_thigh = np.column_stack([accx_right_thigh[0:nb_common_samples], accy_right_thigh[0:nb_common_samples], accz_right_thigh[0:nb_common_samples]])
    mag_imu_right_thigh = np.column_stack([mx_right_thigh[0:nb_common_samples], my_right_thigh[0:nb_common_samples], mz_right_thigh[0:nb_common_samples]])
    gyr_imu_right_thigh = np.column_stack([gyrx_right_thigh[0:nb_common_samples], gyry_right_thigh[0:nb_common_samples], gyrz_right_thigh[0:nb_common_samples]])
    acc_imu_left_thigh = np.column_stack([accx_left_thigh[0:nb_common_samples], accy_left_thigh[0:nb_common_samples], accz_left_thigh[0:nb_common_samples]])
    mag_imu_left_thigh = np.column_stack([mx_left_thigh[0:nb_common_samples], my_left_thigh[0:nb_common_samples], mz_left_thigh[0:nb_common_samples]])
    gyr_imu_left_thigh = np.column_stack([gyrx_left_thigh[0:nb_common_samples], gyry_left_thigh[0:nb_common_samples], gyrz_left_thigh[0:nb_common_samples]])
    acc_imu_right_shank = np.column_stack([accx_right_shank[0:nb_common_samples], accy_right_shank[0:nb_common_samples], accz_right_shank[0:nb_common_samples]])
    mag_imu_right_shank = np.column_stack([mx_right_shank[0:nb_common_samples], my_right_shank[0:nb_common_samples], mz_right_shank[0:nb_common_samples]])
    gyr_imu_right_shank = np.column_stack([gyrx_right_shank[0:nb_common_samples], gyry_right_shank[0:nb_common_samples], gyrz_right_shank[0:nb_common_samples]])
    acc_imu_left_shank = np.column_stack([accx_left_shank[0:nb_common_samples], accy_left_shank[0:nb_common_samples], accz_left_shank[0:nb_common_samples]])
    mag_imu_left_shank = np.column_stack([mx_left_shank[0:nb_common_samples], my_left_shank[0:nb_common_samples], mz_left_shank[0:nb_common_samples]])
    gyr_imu_left_shank = np.column_stack([gyrx_left_shank[0:nb_common_samples], gyry_left_shank[0:nb_common_samples], gyrz_left_shank[0:nb_common_samples]])
    acc_imu_trunk = np.column_stack([accx_trunk[0:nb_common_samples], accy_trunk[0:nb_common_samples], accz_trunk[0:nb_common_samples]])
    mag_imu_trunk = np.column_stack([mx_trunk[0:nb_common_samples], my_trunk[0:nb_common_samples], mz_trunk[0:nb_common_samples]])
    gyr_imu_trunk = np.column_stack([gyrx_trunk[0:nb_common_samples], gyry_trunk[0:nb_common_samples], gyrz_trunk[0:nb_common_samples]])
    
    # Applies scale and offset 
    for i in range(0, nb_common_samples):
        mag_imu_right_thigh[i,:]=  np.transpose(np.dot(scale_mag_right_thigh,np.transpose((mag_imu_right_thigh[i,:]-np.transpose(bias_mag_right_thigh)))))
        mag_imu_left_thigh[i,:]=  np.transpose(np.dot(scale_mag_left_thigh,np.transpose((mag_imu_left_thigh[i,:]-np.transpose(bias_mag_left_thigh)))))
        mag_imu_right_shank[i,:]=  np.transpose(np.dot(scale_mag_right_shank,np.transpose((mag_imu_right_shank[i,:]-np.transpose(bias_mag_right_shank)))))
        mag_imu_left_shank[i,:]=  np.transpose(np.dot(scale_mag_left_shank,np.transpose((mag_imu_left_shank[i,:]-np.transpose(bias_mag_left_shank)))))
        mag_imu_trunk[i,:]=  np.transpose(np.dot(scale_mag_trunk,np.transpose((mag_imu_trunk[i,:]-np.transpose(bias_mag_trunk)))))
       
   
    ###########################################      
    # Geometrical calib (q_offset computation)        
    ###########################################
       
    data_static_right_thigh = np.hstack((acc_imu_right_thigh[0:1200], mag_imu_right_thigh[0:1200], gyr_imu_right_thigh[0:1200]))
    data_static_left_thigh = np.hstack((acc_imu_left_thigh[0:1200], mag_imu_left_thigh[0:1200], gyr_imu_left_thigh[0:1200]))
    data_static_right_shank = np.hstack((acc_imu_right_shank[0:1200], mag_imu_right_shank[0:1200], gyr_imu_right_shank[0:1200]))
    data_static_left_shank = np.hstack((acc_imu_left_shank[0:1200], mag_imu_left_shank[0:1200], gyr_imu_left_shank[0:1200]))
    data_static_trunk = np.hstack((acc_imu_trunk[0:1200], mag_imu_trunk[0:1200], gyr_imu_trunk[0:1200]))
    
    q_offset_right = \
            calib_geom.compute(data_static_right_thigh, data_static_right_shank)
    q_offset_left = \
            calib_geom.compute(data_static_left_thigh, data_static_left_shank)

    ################################
    # Quaternions computation #
    ################################

    # Observers initiations
    observer_right_thigh = martin.martin_ahrs()
    observer_left_thigh = martin.martin_ahrs()
    observer_right_shank = martin.martin_ahrs()
    observer_left_shank = martin.martin_ahrs()
    observer_trunk = martin.martin_ahrs()
    
#    euler_ref = np.zeros((len(acc_imu_ref),3))
    
    # Quaternions initiation
    q_right_thigh = np.zeros((nb_common_samples,4))
    q_right_shank = np.zeros((nb_common_samples,4))
    q_left_thigh = np.zeros((nb_common_samples,4))
    q_left_shank = np.zeros((nb_common_samples,4))
    q_trunk = np.zeros((nb_common_samples,4))
    
    # Init data
    data_init_right_thigh = np.mean(data_static_right_thigh[:,0:10],0)
    data_init_left_thigh = np.mean(data_static_left_thigh[:,0:10],0)
    data_init_right_shank = np.mean(data_static_right_shank[:,0:10],0)
    data_init_left_shank = np.mean(data_static_left_shank[:,0:10],0)
    data_init_trunk = np.mean(data_static_trunk[:,0:10],0)
    
    q_right_thigh[0,:] = observer_right_thigh.init_observer(data_init_right_thigh)  #build the observer from the mean values of the geom calib position
    q_left_thigh[0,:] = observer_left_thigh.init_observer(data_init_left_thigh)  #build the observer from the mean values of the geom calib position
    q_right_shank[0,:] = observer_right_shank.init_observer(data_init_right_shank)  #build the observer from the mean values of the geom calib position
    q_left_shank[0,:] = observer_left_shank.init_observer(data_init_left_shank)  #build the observer from the mean values of the geom calib position
    q_trunk[0,:] = observer_trunk.init_observer(data_init_trunk)  #build the observer from the mean values of the geom calib position
    
    for i in range(0, nb_common_samples-1):
        q_right_thigh[i+1]= observer_right_thigh.update(np.hstack([acc_imu_right_thigh[i,:],mag_imu_right_thigh[i,:], gyr_imu_right_thigh[i,:]]), 0.005)
        q_left_thigh[i+1]= observer_left_thigh.update(np.hstack([acc_imu_left_thigh[i,:],mag_imu_left_thigh[i,:], gyr_imu_left_thigh[i,:]]), 0.005)
        q_right_shank[i+1]= observer_right_shank.update(np.hstack([acc_imu_right_shank[i,:],mag_imu_right_shank[i,:], gyr_imu_right_shank[i,:]]), 0.005)
        q_left_shank[i+1]= observer_left_shank.update(np.hstack([acc_imu_left_shank[i,:],mag_imu_left_shank[i,:], gyr_imu_left_shank[i,:]]), 0.005)
        q_trunk[i+1]= observer_trunk.update(np.hstack([acc_imu_trunk[i,:],mag_imu_trunk[i,:], gyr_imu_trunk[i,:]]), 0.005)
        
    
    ###########################################################################
    # Compute angles from the quaternions
    ###########################################################################
    
    knee_angle_right = np.zeros((nb_common_samples,1))
    knee_angle_left = np.zeros((nb_common_samples,1))
   
    
    for i in range(0, nb_common_samples-1):
        [knee_angle_left[i], _] = \
            goniometer.compute(q_left_thigh[i], q_left_shank[i], q_offset_left.reshape(4,))
        [knee_angle_right[i], _] = \
            goniometer.compute(q_right_thigh[i], q_right_shank[i], q_offset_right.reshape(4,))
    
    # Frame change from NEDown to initial frame    
    conj_q_init_trunk = nq.conjugate(q_trunk[1200, :])
    euler_trunk = np.zeros((nb_common_samples,3))
    for i in range(0, nb_common_samples-1):
        q_trunk[i] = nq.mult(conj_q_init_trunk, q_trunk[i])
        euler_trunk[i] = quat2euler(q_trunk[i])
   
    # Plots
#    plt.figure()
#    plt.hold(True)
#    plt.plot(euler_trunk[:,2]*180/pi)
#    plt.plot(knee_angle_right*180/pi)
#    plt.plot(knee_angle_left*180/pi)
    
     # Save the calculated quaternions to a .mat file
    quat_dict={}    
    quat_dict['knee_angle_right'] = knee_angle_right
    quat_dict['knee_angle_left'] = knee_angle_left
    quat_dict['quaternion_trunk'] = q_trunk
    quat_dict['euler_trunk_ZYX'] = euler_trunk
    
    sio.savemat('export_'+str(trial_number)+'.mat', quat_dict)

if __name__ == '__main__':
    tug() 