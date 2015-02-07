# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 11:25:46 2014

@author: bsijober

Calib for IMU sensors data
"""
import numpy as np
from sensbiotk.transforms3d import quaternions as nq
import sensbiotk.algorithms.madgwick_ahrs as madgwick
import sensbiotk.algorithms.martin_ahrs as martin

def compute(data_imu0, data_imu1):
    
    """ Compute an "offset" quaternion between two supposed aligned quaternions
    
    Parameters :
    ------------
    data_imu0  : numpy array of float
                 the IMU column stacked reference position data [ACC MAG GYR]
    data_imu1 : numpy array of float
                 the IMU column stacked reference position data [ACC MAG GYR]

    Returns
    -------
    q_offset : quaternion [w, x, y, z]
                 the offset quaternion between IMU0 and IMU1
    """

    # Averages the data on the reference position
    data_ref_imu0 = np.mean(data_imu0[:,0:10],0)
    data_ref_imu1 = np.mean(data_imu1[:,0:10],0)

    # madgwick calculation
#    q_init=[1, 0, 0, 0]
#    q0 = madgwick.update(q_init, data_ref_imu0)
#    q1 = madgwick.update(q_init, data_ref_imu1)   

    # Uses martin salaun for calculating the two quaternions
    init0 = martin.martin_ahrs()
    init1 = martin.martin_ahrs()
    q0 = init0.init_observer(data_ref_imu0)
    q1 = init1.init_observer(data_ref_imu1)        
    
    q_offset=nq.mult(np.transpose(nq.conjugate(q0)),np.transpose(q1)) # q_offset = conj(q0) x q1
    
    return q_offset