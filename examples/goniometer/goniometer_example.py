# -*- coding: utf-8 -*-
"""
Goniometer examples using two IMUs.

Three files are needed by IMU :
1/ calib sensor file (for computing calibrations parameters)
2/ calib geom file (static position for initial alignement of the sensors)
3/ trial file, in this example : stand to sit to stand to sit (0, 90°, 0, 90°)

This example uses martin_ahrs algorithm for quaternions computation,
and the calibration (geom and sensors) scripts contained in sensbiotk.


@author: bsijober
"""

import numpy as np 
import matplotlib.pyplot as plt
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib_geom as calib_geom
import sensbiotk.algorithms.martin_ahrs as martin
import sensbiotk.calib.calib as calib
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.algorithms.goniometer as goniometer
from sensbiotk.transforms3d.eulerangles import quat2euler

close('all')
def goniometer_example():
    
    calib_sensor_shank = 'data/CALIB_SENSORS/1_IMU23_SHANK.csv' #rot
    calib_sensor_thigh = 'data/CALIB_SENSORS/1_IMU22_THIGH.csv' #ref
    calib_geom_shank = 'data/CALIB_GEOM/2_IMU23_SHANK.csv'
    calib_geom_thigh = 'data/CALIB_GEOM/2_IMU22_THIGH.csv'
    trial_file_shank = 'data/STAND_TO_SIT_TO_STAND_TO_SIT/3_IMU23_SHANK.csv'
    trial_file_thigh = 'data/STAND_TO_SIT_TO_STAND_TO_SIT/3_IMU22_THIGH.csv'
    
    ######################################################
    # Sensors (scale/offset) calib parameters computation
    ######################################################
    [params_acc_ref, params_mag_ref, params_gyr_ref] = \
           calib.compute(imuNumber=22 ,filepath=calib_sensor_thigh, param = 3)
           
    [params_acc_rot, params_mag_rot, params_gyr_rot] = \
           calib.compute(imuNumber=23 ,filepath=calib_sensor_shank, param = 3)  
       
    scale_acc_ref = params_acc_ref[1:4,:]
    bias_acc_ref = params_acc_ref[0,:]
    scale_mag_ref = params_mag_ref[1:4,:]
    bias_mag_ref = params_mag_ref[0,:]
    scale_gyr_ref = params_gyr_ref[1:4,:]
    bias_gyr_ref = params_gyr_ref[0,:]       
    
    scale_acc_rot = params_acc_rot[1:4,:]
    bias_acc_rot = params_acc_rot[0,:]
    scale_mag_rot = params_mag_rot[1:4,:]
    bias_mag_rot = params_mag_rot[0,:]
    scale_gyr_rot = params_gyr_rot[1:4,:]
    bias_gyr_rot = params_gyr_rot[0,:]       
    
    ###########################################      
    # Geometrical calib (q_offset computation)        
    ###########################################
    # load data from the recording calib
    [time_imu_calib_ref, accx_calib_ref, accy_calib_ref, accz_calib_ref, mx_calib_ref,\
        my_calib_ref, mz_calib_ref, gyrx_calib_ref, gyry_calib_ref, gyrz_calib_ref] = \
            load_foxcsvfile(calib_geom_thigh)
    
    [time_imu_calib_rot, accx_calib_rot, accy_calib_rot, accz_calib_rot, mx_calib_rot,\
        my_calib_rot, mz_calib_rot, gyrx_calib_rot, gyry_calib_rot, gyrz_calib_rot] = \
            load_foxcsvfile(calib_geom_shank)
    
    ############################
    acc_imu_calib_ref = np.column_stack([accx_calib_ref, accy_calib_ref, accz_calib_ref])
    mag_imu_calib_ref = np.column_stack([mx_calib_ref, my_calib_ref, mz_calib_ref])
    gyr_imu_calib_ref = np.column_stack([gyrx_calib_ref, gyry_calib_ref, gyrz_calib_ref])
    # Applies scale and offset on raw calib trial data (ref)
    for i in range(0,len(acc_imu_calib_ref)-1):
        acc_imu_calib_ref[i,:]=  np.transpose(np.dot(scale_acc_ref,np.transpose((acc_imu_calib_ref[i,:]-np.transpose(bias_acc_ref)))))
        mag_imu_calib_ref[i,:]=  np.transpose(np.dot(scale_mag_ref,np.transpose((mag_imu_calib_ref[i,:]-np.transpose(bias_mag_ref)))))
        gyr_imu_calib_ref[i,:]=  np.transpose(np.dot(scale_gyr_ref,np.transpose((gyr_imu_calib_ref[i,:]-np.transpose(bias_gyr_ref)))))
    
    ############################
    acc_imu_calib_rot = np.column_stack([accx_calib_rot, accy_calib_rot, accz_calib_rot])
    mag_imu_calib_rot = np.column_stack([mx_calib_rot, my_calib_rot, mz_calib_rot])
    gyr_imu_calib_rot = np.column_stack([gyrx_calib_rot, gyry_calib_rot, gyrz_calib_rot])
    # Applies scale and offset on raw calib trial data (rot)
    for i in range(0,len(acc_imu_calib_rot)-1):
        acc_imu_calib_rot[i,:]=  np.transpose(np.dot(scale_acc_rot,np.transpose((acc_imu_calib_rot[i,:]-np.transpose(bias_acc_rot)))))
        mag_imu_calib_rot[i,:]=  np.transpose(np.dot(scale_mag_rot,np.transpose((mag_imu_calib_rot[i,:]-np.transpose(bias_mag_rot)))))
        gyr_imu_calib_rot[i,:]=  np.transpose(np.dot(scale_gyr_rot,np.transpose((gyr_imu_calib_rot[i,:]-np.transpose(bias_gyr_rot)))))
    ############################
        
    data_ref_calib_geom = np.hstack((acc_imu_calib_ref, mag_imu_calib_ref, gyr_imu_calib_ref))
    data_rot_calib_geom = np.hstack((acc_imu_calib_rot, mag_imu_calib_rot, gyr_imu_calib_rot))
    
    q_offset = \
            calib_geom.compute(data_ref_calib_geom, data_rot_calib_geom)
    
    #######################
    # Trial data loading
    #######################
    # Loads trial data (ref imu thigh)
    [time_imu_ref, accx_ref, accy_ref, accz_ref, mx_ref, my_ref, mz_ref, gyrx_ref, gyry_ref, gyrz_ref] = \
            load_foxcsvfile(trial_file_thigh)
            
    # Loads trial data (rot imu shank)
    [time_imu_rot, accx_rot, accy_rot, accz_rot, mx_rot, my_rot, mz_rot, gyrx_rot, gyry_rot, gyrz_rot] = \
            load_foxcsvfile(trial_file_shank)
    
    
    ################################
    # q_ref quaternion computation #
    ################################
    # Applies the Scale and Offset to data ref
    acc_imu_ref = np.column_stack([accx_ref, accy_ref, accz_ref])
    mag_imu_ref = np.column_stack([mx_ref, my_ref, mz_ref])
    gyr_imu_ref = np.column_stack([gyrx_ref, gyry_ref, gyrz_ref])
    
    # Quaternions calculation q_ref (thigh)
    observer_ref = martin.martin_ahrs()
    euler_ref = np.zeros((len(acc_imu_ref),3))
    q_ref = np.zeros((len(acc_imu_ref),4))
    
    data_ref_imu0 = np.mean(data_ref_calib_geom[:,0:10],0)
    data_ref_imu1 = np.mean(data_rot_calib_geom[:,0:10],0)
    
    #q_ref[0,:] = observer_ref.init_observer(np.hstack([acc_imu_ref[0,:],mag_imu_ref[0,:], gyr_imu_ref[0,:]]))
    q_ref[0,:] = observer_ref.init_observer(data_ref_imu0)  #build the observer from the mean values of the geom calib position
    
    for i in range(1,len(acc_imu_ref)-1):
    #    acc_imu_ref[i,:]= np.transpose(np.dot(scale_acc_ref,np.transpose((acc_imu_ref[i,:]-np.transpose(bias_acc_ref)))))
        mag_imu_ref[i,:]=  np.transpose(np.dot(scale_mag_ref,np.transpose((mag_imu_ref[i,:]-np.transpose(bias_mag_ref)))))
        gyr_imu_ref[i,:]=  np.transpose(np.dot(scale_gyr_ref,np.transpose((gyr_imu_ref[i,:]-np.transpose(bias_gyr_ref)))))
        q_ref[i+1]= observer_ref.update(np.hstack([acc_imu_ref[i,:],mag_imu_ref[i,:], gyr_imu_ref[i,:]]), 0.005)
        euler_ref[i]=quat2euler(q_ref[i+1])
    
    
    ################################
    # q_rot quaternion computation #
    ################################   
    # Applies the Scale and Offset to data rot
    acc_imu_rot = np.column_stack([accx_rot, accy_rot, accz_rot])
    mag_imu_rot = np.column_stack([mx_rot, my_rot, mz_rot])
    gyr_imu_rot = np.column_stack([gyrx_rot, gyry_rot, gyrz_rot])
    
    # Quaternions calculation q_rot (shank)
    observer_rot = martin.martin_ahrs()
    euler_rot = np.zeros((len(acc_imu_rot),3))
    q_rot = np.zeros((len(acc_imu_rot),4))
    #q_rot[0,:] = observer_rot.init_observer(np.hstack([acc_imu_rot[0,:],mag_imu_rot[0,:], gyr_imu_rot[0,:]]))
    q_rot[0,:] = observer_rot.init_observer(data_ref_imu1) #build the observer from the mean values of the geom calib position
    
    for i in range(0,len(acc_imu_rot)-1):
    #    acc_imu_rot[i,:]= np.transpose(np.dot(scale_acc_rot,np.transpose((acc_imu_rot[i,:]-np.transpose(bias_acc_rot)))))
        mag_imu_rot[i,:]=  np.transpose(np.dot(scale_mag_rot,np.transpose((mag_imu_rot[i,:]-np.transpose(bias_mag_rot)))))
        gyr_imu_rot[i,:]=  np.transpose(np.dot(scale_gyr_rot,np.transpose((gyr_imu_rot[i,:]-np.transpose(bias_gyr_rot)))))
        q_rot[i+1]= observer_rot.update(np.hstack([acc_imu_rot[i,:],mag_imu_rot[i,:], gyr_imu_rot[i,:]]), 0.005)
        euler_rot[i]= quat2euler(q_rot[i+1])
    
    ###########################################################################
    
    # Compute angles from the two quaternions
    angle = np.zeros((len(q_ref)-1))
    rot_axis = np.zeros((len(q_ref),3))
    euler = np.zeros((len(q_ref),3))
    
    for i in range(0,len(q_ref)-1):
        [angle[i], rot_axis[i]] = \
            goniometer.compute(q_ref[i], q_rot[i], q_offset.reshape(4,))
        euler[i]=quat2euler(np.hstack((angle[i],rot_axis[i])))
    
    
    f, axis = plt.subplots(2, sharex=True)
    # Plot angle
    axis[0].plot(angle*180/np.pi, label='angle')
    axis[0].set_title('Angle')
    axis[0].set_ylabel('deg')
    axis[0].legend()
    # Plot rot axis
    axis[1].plot(rot_axis)
    axis[1].set_title('Rot. Axis')
    axis[1].legend(('x','y','z'))

if __name__ == '__main__':
    goniometer_example() 