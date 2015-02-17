# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 16:11:05 2015

@author: bsijober
"""

import numpy as np
from sensbiotk.algorithms import martin_ahrs
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib_mag as calib_mag
from sensbiotk.transforms3d.eulerangles import quat2euler
import sensbiotk.transforms3d.quaternions as nq
import matplotlib.pyplot as plt

data_calib_file = "data/CALIB/10_IMU1_HEAD.csv"
imu_number = 1
#CALIBFILE= "data/simple_rotation_v2/CalibrationFileIMU5.txt"
data_file = "data/3/3_IMU1_HEAD.csv"

def plot_quat(title, timu, qw, qx, qy, qz):
    """ Plot quaternion
    """
    plt.figure()
    plt.title(title+" Quaternion")
    plt.plot(timu, qw)
    plt.plot(timu, qx)
    plt.plot(timu, qy)
    plt.plot(timu, qz)
    plt.legend(('qw', 'qx', 'qy', 'qz'))
    return


def plot_euler(title, time, x, y, z): 
    """ Plot euler angles
    """
    plt.figure()
    plt.title(title+" Euler angles")
    plt.plot(time, x*180/np.pi)
    plt.plot(time, y*180/np.pi)
    plt.plot(time, z*180/np.pi)
    plt.legend(('e_x', 'e_y', 'e_z'))
    return

def calib_mag_param(data_calib_file):
    """ Compute mag calibration parameters
    """
    [offset_mag, scale_mag] = \
            calib_mag.compute(data_calib_file)

    return [offset_mag, scale_mag]


def normalize_data(data,  param_calib):
    """ Normalize_data (applies offset and scale)
    """
    scale = param_calib[1:4,:]
    bias = param_calib[0,:]
    data_n = np.transpose(np.dot(scale,np.transpose((data-np.transpose(bias)))))
    
    return data_n

def load_data(data_file):
    ''' Load the recording data
    '''
    [time_imu, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
        load_foxcsvfile(data_file)
    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([mx, my, mz])
    gyr_imu = np.column_stack([gyrx, gyry, gyrz])
    
    return [time_imu, acc_imu, mag_imu, gyr_imu]

def run():
    """ run example
    """
    # Load data
    [_, _, mag_calib, _] = load_data(data_calib_file)      
    
    # Compute calib params
    [offset_mag, scale_mag] = calib_mag_param(mag_calib)
    params_mag = np.vstack((offset_mag, scale_mag))

    # Load data
    [time_imu, acc_imu, mag_imu, gyr_imu] = load_data(data_file)    
    
    # Init output
    quat = np.zeros((len(acc_imu), 4))
    quat_corr = np.zeros((len(acc_imu), 4))
    euler = np.zeros((len(acc_imu), 3))
    observer = martin_ahrs.martin_ahrs()
    data_init = np.mean(np.hstack([acc_imu[0:100, :], mag_imu[0:100, :], gyr_imu[0:100, :]]), 0) # mean of the first static 2 seconds
    quat[0] = observer.init_observer(data_init)
    
    # Computation loop
    for i in range(0, len(acc_imu)):
        # Applies the Scale and Offset to data
        mag_imu[i,:] = normalize_data(mag_imu[i,:], params_mag)
        # Filter call
        quat[i] = observer.update(np.hstack([acc_imu[i, :], mag_imu[i, :], gyr_imu[i, :]]), 0.005)

    conj_q_init = nq.conjugate(quat[100, :])
    for i in range(0, len(acc_imu)-1):
        quat_corr[i+1] = nq.mult(conj_q_init,quat[i+1])
        euler[i]=quat2euler(quat_corr[i+1])
      
     
     #load vicon data
    head_angle_vicon = np.loadtxt('data/3/head_angle_vicon.txt')
    
    time_delay = 0.3
    #Plot results
    plt.hold(True) 
    plt.plot(np.arange(0, len(head_angle_vicon)/100., 0.01), head_angle_vicon)
    plt.plot(time_imu - time_delay, euler[:,0]*180/np.pi-6,'k--',linewidth='1.5')
    plt.legend(('head_angle_vicon','head_angle_imu'))
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (deg)')

if __name__ == '__main__':
    run() 
    plt.show()


