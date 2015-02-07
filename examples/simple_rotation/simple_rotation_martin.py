
# -*- coding: utf-8 -*-
"""
Reconstruction angles example comparison
"""

import numpy as np
from sensbiotk.algorithms import martin_ahrs
import sensbiotk.algorithms.mahony_ahrs as mahony
from sensbiotk.io.iofox import load_foxcsvfile
from sensbiotk.io.ahrs import save_ahrs_csvfile
import sensbiotk.calib.calib as calib
from sensbiotk.transforms3d.eulerangles import quat2euler
from sensbiotk.transforms3d.eulerangles import quat2euler2
from sensbiotk.transforms3d.quaternions import quat2mat
from visual import *
import scipy.io
import matplotlib.pyplot as plt

DATACALIBFILE = "data/simple_rotation_v2/CALIB.csv"
#CALIBFILE= "data/simple_rotation_v2/CalibrationFileIMU5.txt"
#DATAFILE = "data/simple_rotation_v2/ROT90_Y.csv"
CALIBFILE= "data/simple_rotation/CalibrationFileIMU4.txt"
DATAFILE = "data/simple_rotation/90_around_x.csv"

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


def plot_euler(title, time, phi, theta, psi): 
    """ Plot euler angles
    """
    plt.figure()
    plt.title(title+" Euler angles")
    plt.plot(time, phi*180/math.pi)
    plt.plot(time, theta*180/math.pi)
    plt.plot(time, psi*180/math.pi)
    plt.legend(('e_x', 'e_y', 'e_z'))
    return

def calib_param(compute = False):
    """ Load or compute calibration parameters
    """
    if compute == True :
        [params_acc, params_mag, params_gyr] = \
            calib.compute(imuNumber=5 ,filepath=DATACALIBFILE, param = 3)
    else:
        [params_acc, params_mag, params_gyr] = \
            calib.load_param(CALIBFILE)

    return [params_acc, params_mag, params_gyr]


def normalize_data(data,  param_calib):
    """ normalize_data
    """
    scale = param_calib[1:4,:]
    bias = param_calib[0,:]
    data_n = np.transpose(np.dot(scale,np.transpose((data-np.transpose(bias)))))
    
    return data_n


def run_example(typ_filter = "martin"):
    """ run example : "mahony" or "martin"
    """
    # Compute (True) or load (False
    [params_acc, params_mag, params_gyr] = calib_param(compute = False)
    # Load the recording data 
    [time_imu, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
        load_foxcsvfile(DATAFILE)
    acc_imu = np.column_stack([accx, accy, accz])
    mag_imu = np.column_stack([mx, my, mz])
    gyr_imu = np.column_stack([gyrx, gyry, gyrz])
    # Init output
    quat = np.zeros((len(acc_imu),4))
    euler = np.zeros((len(acc_imu),3))
    observer = martin_ahrs.martin_ahrs()

    # Computation loop
    for i in range(0,len(acc_imu)):
        # Applies the Scale and Offset to data
        acc_imu[i,:] = normalize_data(acc_imu[i,:], params_acc)
        mag_imu[i,:] = normalize_data(mag_imu[i,:], params_mag)
        gyr_imu[i,:] = normalize_data(gyr_imu[i,:], params_gyr)
        # Filter call
        if i == 0:
            if typ_filter == "mahony":
                quat[0,:]=[1, 0, 0, 0]
            else:
                quat[0]=observer.init_observer(np.hstack([acc_imu[0,:],mag_imu[0,:], gyr_imu[0,:]]))
        else: 
            if typ_filter == "mahony":
                quat[i]= mahony.update(quat[i-1],np.hstack([acc_imu[i,:],mag_imu[i,:], gyr_imu[i,:]]))
                euler[i]=quat2euler(quat[i])
            else:
                quat[i]=observer.update(np.hstack([acc_imu[i,:],mag_imu[i,:], gyr_imu[i,:]]), 0.005)
                euler[i]=quat2euler(quat[i])
    
    #Plot results
    plot_quat(typ_filter, time_imu,\
                     quat[:,0], quat[:,1], quat[:,2], quat[:,3])
    if typ_filter == "mahony":
        plot_euler(typ_filter, time_imu,\
                       euler[:,2], euler[:,1], euler[:,0])
    else:
        plot_euler(typ_filter, time_imu,\
                       euler[:,2], euler[:,1], euler[:,0])
    

if __name__ == '__main__':
    run_example("martin") 
    run_example("mahony") 
    plt.show()
