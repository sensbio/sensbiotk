# -*- coding: utf-8 -*-
"""
Quaternion & Euler angles calculation and 3D visualization

@author: bsijober
"""

import numpy as np 
import matplotlib.pyplot as plt
import sensbiotk.algorithms.madgwick_ahrs as madgwick
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib as calib
from sensbiotk.transforms3d.eulerangles import quat2euler
import sensbiotk.transforms3d.quaternions as nq
from visual import *
import scipy.io as sio

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

close('all')
def VPython_quaternion_3D():

    # Compute 
#    [params_acc, params_mag, params_gyr] = \
#        calib.compute(imuNumber=6 ,filepath="data/CALIB.csv", param = 3)

    [params_acc, params_mag, params_gyr] = \
        calib.load_param("data/CalibrationFileIMU6.txt")

    # Load the recording data 
    [time_imu, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
        load_foxcsvfile("data/1_IMU6_RIGHT_FOOT.csv")

    # Applies the Scale and Offset to data
    scale_acc = params_acc[1:4,:]
    bias_acc = params_acc[0,:]
    scale_mag = params_mag[1:4,:]
    bias_mag = params_mag[0,:]
    scale_gyr = params_gyr[1:4,:]
    bias_gyr = params_gyr[0,:]       
    
    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([mx, my, mz])
    gyr_imu = np.column_stack([gyrx, gyry, gyrz])
    
    quaternion = np.zeros((len(acc_imu),4))
    euler = np.zeros((len(acc_imu),3))
    
    quaternion[0,:]=[1, 0, 0, 0]
        
    for i in range(0,len(acc_imu)-1):
        acc_imu[i,:]= np.transpose(np.dot(scale_acc,np.transpose((acc_imu[i,:]-np.transpose(bias_acc)))))
        mag_imu[i,:]=  np.transpose(np.dot(scale_mag,np.transpose((mag_imu[i,:]-np.transpose(bias_mag)))))
        gyr_imu[i,:]=  np.transpose(np.dot(scale_gyr,np.transpose((gyr_imu[i,:]-np.transpose(bias_gyr)))))
        quaternion[i+1]= madgwick.update(quaternion[i],np.hstack([acc_imu[i,:],mag_imu[i,:], gyr_imu[i,:]]))
        euler[i]=quat2euler(quaternion[i+1])
    
    #######################
    # Plots
    ####################### 
    dataVicon = np.loadtxt('data/RIGHT_FOOT.txt',skiprows=4)
    time_vicon = dataVicon[:,0]
    euler_vicon= np.zeros((len(time_vicon),3))
    quat_offset = np.hstack([dataVicon[0,7], dataVicon[0,4], dataVicon[0,5], dataVicon[0,6]])
    for i in range(1, len(time_vicon)-1):
        quat_vicon = np.hstack([dataVicon[i,7], dataVicon[i,4], dataVicon[i,5], dataVicon[i,6]])
        euler_vicon[i] = quat2euler(nq.mult(nq.conjugate(quat_offset),quat_vicon))
        
    #Z    
    plt.figure()
    plt.hold(True)    
    plt.plot(time_imu-(0.2), euler[:,0]*180/pi)
    plt.plot(time_vicon, euler_vicon[:,0]*180/pi)
    plt.legend(('z_imu','z_vicon'))
    xlabel('time (s)')
    ylabel('angle (deg)')
    #Y
    plt.figure()
    plt.hold(True)
    plt.plot(time_imu-(0.2), euler[:,1]*180/pi)
    plt.plot(time_vicon, euler_vicon[:,1]*180/pi)
    plt.legend(('y_imu','y_vicon'))
    xlabel('time (s)')
    ylabel('angle (deg)')
    plt.show()
    #X
    plt.figure()
    plt.hold(True)
    plt.plot(time_imu-(0.2), euler[:,2]*180/pi)
    plt.plot(time_vicon, euler_vicon[:,2]*180/pi)
    plt.legend(('x_imu','x_vicon'))
    xlabel('time (s)')
    ylabel('angle (deg)')
    plt.show()
    
    quat_dict={}    
    quat_dict['quaternion'] = quaternion
    sio.savemat('quaternion_madgwick.mat', quat_dict)

if __name__ == '__main__':
    VPython_quaternion_3D() 
