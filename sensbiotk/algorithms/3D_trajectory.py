# -*- coding: utf-8 -*-
''' Module implementing 3D trajectory of the foot computation algorithms subparts.
(alpha version, extracted from a global script, need to be completed, tested and further documented.)
'''

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import sensbiotk.calib.calib_geom as calib_geom
import sensbiotk.algorithms.martin_ahrs as martin
import sensbiotk.calib.calib as calib
from sensbiotk.transforms3d.eulerangles import quat2euler
from sensbiotk.transforms3d.eulerangles import quat2euler4
from sensbiotk.transforms3d.eulerangles import euler2quat
from sensbiotk.transforms3d import quaternions as nq
from tkFileDialog import askopenfilename
import os
import re
import scipy.io as sio
import compute_martin_angle
from scipy import signal

from sensbiotk.transforms3d import quaternions as q
from sensbiotk.transforms3d import eulerangles as euler



def acc_filtering(fs = 200, acc_x, acc_y, acc_z):
    ''' HP & LP filters for 3D accelerometer data

    Parameters
    ----------
    fs : integer
    sampling rate in Hz
    acc_x : array
    acc_y : array
    acc_z : array

    Returns
    -------
    acc_x, acc_y, acc_z : array
   '''
#        # HP filter data
#        filtCutOff = 0.001
#        [b, a] = signal.butter(1, filtCutOff/(fs/2.), btype='high') # highpass filter for removing near-constant component
        
        # LP filter accelerometer data
    filtCutOff = 5
    
    [b, a] = signal.butter(1, filtCutOff/(fs/2.), btype='low')
    acc_x = signal.filtfilt(b, a, acc_x, axis=0)
    acc_y = signal.filtfilt(b, a, acc_y, axis=0)
    acc_z = signal.filtfilt(b, a, acc_z, axis=0)
    return acc_x, acc_y, acc_z

        
def compute_trajs(acc_x, acc_y, acc_z, q_imu, starts, stops):
    ''' Compute trajectories from 3D accelerometer data, quaternion and starts/stop stride marks

    Parameters
    ----------
    acc_x : array
    acc_y : array
    acc_z : array
    q_imu : array
    The quaternion array corresponding to the IMU orientation in global frame.
    starts: array
    The starts sample marks for bounding integration, detected from the 
    stationary periods (start and stop of the strides) 
    stops: array
    The stops sample marks for bounding integration, detected from the 
    stationary periods (start and stop of the strides) 


    Returns
    -------
    acc_x, acc_y, acc_z : array
   '''
        for i in range(0,len(starts)-1,2):
          acc_x_traj = acc_x[starts[i]:stops[i]]
          acc_y_traj = acc_y[starts[i]:stops[i]]
          acc_z_traj = acc_z[starts[i]:stops[i]]
          quat_traj = q_imu[starts[i]:stops[i]]
        
          [acc_x_traj_wg, acc_y_traj_wg, acc_z_traj_wg] = rm_gravity_traj(acc_x_traj, acc_y_traj, acc_z_traj, quat_traj)
          integrate_traj_manually(acc_x_traj_wg, acc_y_traj_wg, acc_z_traj_wg)
        

     
def find_stationary_period(acc_threshold = 10.6, gyr_threshold = 80, acc_data, gyr_data):
    ''' Find stationary periods (start,stop) to partition gait

    Parameters
    ----------
    acc_threshold : integer
    gyr_threshold : integer
    acc_data: array(,3)
    gyr_data: array(,3)

    Returns
    -------
    stationary_period : array
   '''
    acc_magnitude = np.linalg.norm(acc_data)
    gyr_magnitude = np.linalg.norm(gyr_data)*180/np.pi
    stationary_period = np.where(acc_magnitude <= acc_threshold and gyr_magnitude <= gyr_threshold)
    
    return stationary_period

       

def rm_3d_gravity(acc_x, acc_y, acc_z, q):
        g = np.array([9.81, 0, 0])
        g_prim = q.rotate_vector(g, q.conjugate(q))
        
        acc_x_wg = acc_x - g_prim[0]
        acc_y_wg = acc_y - g_prim[1]
        acc_z_wg = acc_z - g_prim[2]
        
        return acc_x_wg, acc_y_wg, acc_z_wg

def rm_3d_gravity_laud(acc_x, acc_y, acc_z, rad_angles):
        acc_y_wg = np.cos(-rad_angles[0])*acc_y - np.sin(-rad_angles[0])*acc_x 
        acc_x_wg = np.sin(rad_angles[0])*acc_y + np.cos(-rad_angles[0])*acc_x - 9.81     
        acc_z_wg = acc_z
    

def integrate_traj():
        vel_z_traj = integrate.cumtrapz(acc_z_traj, time_traj, axis = 0, initial = 0)
        vel_y_traj = integrate.cumtrapz(acc_y_traj, time_traj, axis = 0, initial = 0)
        vel_x_traj = integrate.cumtrapz(acc_x_traj, time_traj, axis = 0, initial = 0)
        
        z_traj = integrate.cumtrapz(vel_z_traj, time_traj, axis = 0, initial = 0)
        y_traj = integrate.cumtrapz(vel_y_traj, time_traj, axis = 0, initial = 0)
        x_traj = integrate.cumtrapz(vel_x_traj, time_traj, axis = 0, initial = 0)
     
def integrate_traj_manually( acc_x_traj, acc_y_traj, acc_z_traj):  
        vel_z_traj = np.zeros(len(acc_z_traj))
        vel_y_traj = np.zeros(len(acc_y_traj))
        vel_x_traj = np.zeros(len(acc_x_traj))
        z_traj = np.zeros(len(vel_z_traj))
        y_traj = np.zeros(len(vel_y_traj))
        x_traj = np.zeros(len(vel_x_traj))
        
        for t in range(1,len(vel_z_traj)):
            vel_z_traj[t] = vel_z_traj[t-1] + acc_z_traj[t] * (time_imu[t]-time_imu[t-1])
            vel_y_traj[t] = vel_y_traj[t-1] + acc_y_traj[t] * (time_imu[t]-time_imu[t-1])
            vel_x_traj[t] = vel_x_traj[t-1] + acc_x_traj[t] * (time_imu[t]-time_imu[t-1])
    
        remove_velocity_drift()

        for t in range(1,len(vel_z_traj)):
            z_traj[t] = z_traj[t-1] + vel_z_traj[t] * (time_imu[t]-time_imu[t-1])
            y_traj[t] = y_traj[t-1] + vel_y_traj[t] * (time_imu[t]-time_imu[t-1])
            x_traj[t] = x_traj[t-1] + vel_x_traj[t] * (time_imu[t]-time_imu[t-1])
#            cum_pos = np.vstack((cum_pos, np.array([x_traj[t] + pos_between_step[0], y_traj[t] + pos_between_step[1], z_traj[t] + pos_between_step[2]])))
        remove_traj_drift()
        for t in range(0,len(vel_z_traj)):
            cum_pos = np.vstack((cum_pos, np.array([x_traj[t] + pos_between_step[0], y_traj[t] + pos_between_step[1], z_traj[t] + pos_between_step[2]])))   
   
#        print('MAX FOOT CLEARANCE:'+str(np.max(np.abs(x_traj))*100) +'cm')
#        print('HEIGHT END:'+str(x_traj[-1]*100)+'cm')
#        print('SL: '+str(np.sqrt(x_traj[-1]*x_traj[-1] + y_traj[-1]*y_traj[-1] + z_traj[-1] * z_traj[-1])*100) + 'cm')
#    
        
    
def remove_velocity_drift():
    rate_z = vel_z_traj[-1] - vel_z_traj[0]
    rate_y = vel_y_traj[-1] - vel_y_traj[0]
    rate_x = vel_x_traj[-1] - vel_x_traj[0]

    vel_z_traj[:] = vel_z_traj[:] - rate_z*np.arange(0,len(vel_z_traj),1)/len(vel_z_traj)
    vel_y_traj[:] = vel_y_traj[:] - rate_y*np.arange(0,len(vel_y_traj),1)/len(vel_y_traj)
    vel_x_traj[:] = vel_x_traj[:] - rate_x*np.arange(0,len(vel_x_traj),1)/len(vel_x_traj)

def remove_traj_drift( x_traj):
    rate_x = x_traj[-1] - x_traj[0]

    x_traj[:] = x_traj[:] - rate_x*np.arange(0,len(x_traj),1)/len(x_traj)
    return x_traj
   

def rotate_acc():
    for i in range(0, len(acc_z_traj)):
        mat = euler.euler2mat(z_traj_angle[i]*np.pi/180, y_traj_angle[i]*np.pi/180, x_traj_angle[i]*np.pi/180)
        [acc_x_traj[i], acc_y_traj[i], acc_z_traj[i]]= np.dot(mat, np.array([acc_x_traj[i], acc_y_traj[i], acc_z_traj[i]]))     

def rotate_traj():
    for i in range(0, len(z_traj_angle)):
        mat = euler.euler2mat(z_traj_angle[i]*np.pi/180, y_traj_angle[i]*np.pi/180, x_traj_angle[i]*np.pi/180)
        [z_traj[i], y_traj[i], x_traj[i]]= np.dot(mat, np.array([z_traj[i], y_traj[i], x_traj[i]]))
                  
        