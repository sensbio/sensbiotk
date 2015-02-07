# -*- coding: utf-8 -*-
"""
Quaternion & Euler angles calculation and 3D visualization

@author: bsijober
"""

import numpy as np 
import matplotlib.pyplot as plt
import sensbiotk.algorithms.martin_ahrs as martin
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib as calib
from sensbiotk.transforms3d.eulerangles import quat2euler
import sensbiotk.transforms3d.quaternions as nq
import scipy.io as sio

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

close('all')
def VPython_quaternion_3D():

    # Compute 
## Example 1
##    [params_acc, params_mag, params_gyr] = \
##        calib.compute(imuNumber=6 ,filepath="data/CALIB.csv", param = 3)
#
#    [params_acc, params_mag, params_gyr] = \
#        calib.load_param("data/CalibrationFileIMU6.txt")

# # Load the recording data 
#    [time_imu, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
#        load_foxcsvfile("data/1_IMU6_RIGHT_FOOT.csv")

#   dataVicon = np.loadtxt('data/RIGHT_FOOT.txt',skiprows=4)
 
# Example 2
    [params_acc, params_mag, params_gyr] = \
        calib.compute(imuNumber=5 ,filepath="data2/CALIB.csv", param = 3)
#
#    [params_acc, params_mag, params_gyr] = \
#        calib.load_param("data2/CalibrationFileIMU5.txt")

 # Load the recording data 
    [time_imu, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
        load_foxcsvfile("data2/5_IMU5_LEFT_FOOT.csv")
   
    dataVicon = np.loadtxt('data2/LEFT_FOOT.txt',skiprows=4)
    time_delay = 3.05
    
## Example 3
#    [params_acc, params_mag, params_gyr] = \
#        calib.compute(imuNumber=5 ,filepath="data3/CALIB.csv", param = 3)
###
##    [params_acc, params_mag, params_gyr] = \
##        calib.load_param("data2/CalibrationFileIMU5.txt")
##
## # Load the recording data 
#    [time_imu, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
#        load_foxcsvfile("data3/4_IMU5_LEFT_FOOT.csv")
##   
#    dataVicon = np.loadtxt('data3/LEFT_FOOT.txt',skiprows=4)
#    time_delay = 0.35

 
    # Applies the Scale and Offset to data
    scale_mag = params_mag[1:4,:]
    bias_mag = params_mag[0,:]
    scale_gyr = params_gyr[1:4,:]
    bias_gyr = params_gyr[0,:]       
    
    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([mx, my, mz])
    gyr_imu = np.column_stack([gyrx, gyry, gyrz])
    
    observer = martin.martin_ahrs()
    
    quaternion = np.zeros((len(acc_imu),4))
    quat_imu_corr = np.zeros((len(acc_imu),4))
    euler = np.zeros((len(acc_imu),3))
    
    data_init = np.mean(np.hstack([acc_imu[0:200,:],mag_imu[0:200,:], gyr_imu[0:200,:]]),0) # mean of the first static 2 seconds

    quaternion[0, :] = observer.init_observer(data_init)
    
    for i in range(1,len(acc_imu)-1):
        mag_imu[i,:]=  np.transpose(np.dot(scale_mag,np.transpose((mag_imu[i,:]-np.transpose(bias_mag)))))
        gyr_imu[i,:]=  np.transpose(np.dot(scale_gyr,np.transpose((gyr_imu[i,:]-np.transpose(bias_gyr)))))
        quaternion[i+1]= observer.update(np.hstack([acc_imu[i,:],mag_imu[i,:], gyr_imu[i,:]]), 0.005)
        
    conj_q_init = nq.conjugate(quaternion[150, :])
    for i in range(1,len(acc_imu)-1):
        quat_imu_corr[i+1] = nq.mult(conj_q_init,quaternion[i+1])
        euler[i]=quat2euler(quat_imu_corr[i+1])

    #######################
    # Plots
    ####################### 
   
    time_vicon = dataVicon[:, 0]
    euler_vicon= np.zeros((len(time_vicon), 3))
    quat_vicon_corr = np.zeros((len(time_vicon), 4))
    quat_offset = np.hstack([dataVicon[0,7], dataVicon[0,4], dataVicon[0,5], dataVicon[0,6]])
    for i in range(1, len(time_vicon)-1):
        quat_vicon = np.hstack([dataVicon[i,7], dataVicon[i,4], dataVicon[i,5], dataVicon[i,6]])
        quat_vicon_corr[i] = nq.mult(nq.conjugate(quat_offset),quat_vicon)        
        euler_vicon[i] = quat2euler(quat_vicon_corr[i])
        
    #Z    
    plt.figure()
    plt.hold(True)    
    plt.plot(time_imu - time_delay, euler[:,0]*180/pi)
    plt.plot(time_vicon, euler_vicon[:,0]*180/pi)
    plt.legend(('z_imu','z_vicon'))
    xlabel('time (s)')
    ylabel('angle (deg)')
    #Y
    plt.figure()
    plt.hold(True)
    plt.plot(time_imu - time_delay, euler[:,1]*180/pi)
    plt.plot(time_vicon, euler_vicon[:,1]*180/pi)
    plt.legend(('y_imu','y_vicon'))
    xlabel('time (s)')
    ylabel('angle (deg)')
    plt.show()
    #X
    plt.figure()
    plt.hold(True)
    plt.plot(time_imu - time_delay, euler[:,2]*180/pi)
    plt.plot(time_vicon, euler_vicon[:,2]*180/pi)
    plt.legend(('x_imu','x_vicon'))
    xlabel('time (s)')
    ylabel('angle (deg)')
    plt.show()

    # Save the calculated quaternions to a .mat file
    quat_dict={}    
    quat_dict['quat_imu_corr'] = quat_imu_corr
    quat_dict['euler_imu_corr_ZYX'] = euler
    quat_dict['quat_vicon_corr'] = quat_vicon_corr
    quat_dict['euler_vicon_corr_ZYX'] = euler_vicon
    quat_dict['time_imu_corr'] = time_imu - time_delay
    quat_dict['time_vicon_corr'] = time_vicon
    
    sio.savemat('export.mat', quat_dict)

if __name__ == '__main__':
    VPython_quaternion_3D() 
