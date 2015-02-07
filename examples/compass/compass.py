# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 14:38:11 2014

@author: bsijober

Example using IMU magnetometer data for visualizing a 2D compass using VPython library.
"""

from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib as calib
from visual import *
import numpy as np


def compass():
    
    # Compute 
#    [_, params_mag, _] = \
#        calib.compute(imuNumber=5 ,filepath="data/1_IMU5_REGLE.csv", param = 3)

    [_, params_mag, _] = \
        calib.load_param("data/CalibrationFileIMU5.txt")

    # Load the recording data 
    [time_imu, _, _, _, mx, my, mz, _, _, _] = \
        load_foxcsvfile("data/2_IMU5_REGLE.csv")

    # Applies the Scale and Offset to data
    scale_mag = params_mag[1:4,:]
    bias_mag = params_mag[0,:]
    
    mag_imu = np.column_stack([mx, my, mz])
       
        
    #######################
    # 3D objects init
    #######################

    scene.title = "VISU COMPASS"
    scene.autocenter = False
    scene.scale = (0.05,0.05,0.05)
    scene.background = (255, 255, 255)
    scene.width = 900
    scene.height = 600
    scene.forward = (0, 0, -1)
    scene.up = (1, 0, 0)

    north_frame = arrow(pos=(0,0,0), axis=(10, 0, 0), shaftwidth=1, color=color.blue)
    west_frame = arrow(pos=(0,0,0), axis=(0, 10, 0), shaftwidth=1, color=color.green)
    est_frame = arrow(pos=(0,0,0), axis=(0, -10, 0), shaftwidth=1, color=color.magenta)
    south_frame = arrow(pos=(0,0,0), axis=(-10, 0, 0), shaftwidth=1, color=color.yellow)
    
    ring(pos=(0, 0, 0), axis=(0 , 0, -1), radius=10, thickness=0.6, color=color.red)
    
    IMU = box(pos=(0, 0, 0), axis = (8, 0, 0), height = 5, width = 3, color = color.black)
     
    angle_display = label(text='Rotation / North : 0 '+u'°', yoffset=0, xoffset=0, line=False, box=False, color=color.blue, height=18, pos=(12, 0, 0))
    
    #######################
    # 3D Animation
    #######################    
       
    angle_north = np.zeros((len(mag_imu)-1,1))     

    for i in range(0,len(mag_imu)-1):
        mag_imu[i,:]=  np.transpose(np.dot(scale_mag,np.transpose((mag_imu[i,:]-np.transpose(bias_mag)))))
        angle_north[i]=np.arctan(mag_imu[i,1]/mag_imu[i,0])+(0.76*pi/180) # declination = 0.76° in Montpellier
    
    rot = np.diff(angle_north, axis = 0)
    rot_cum = np.cumsum(rot)
    for k in range(0,len(rot)):
        rate(200)
        IMU.rotate(origin=(0, 0, 0), angle=rot[k], axis=(0,0,1))
        angle_display.text = 'Rotation / North : '+'%0.2f' %((rot_cum[k])*180/pi)+' '+u'°'
        
    #######################
    # Plots
    ####################### 
    
    figure
    hold(True)    
    plot(rot_cum*180/pi)
    legend(('Rot/North(°)'))
    
if __name__ == '__main__':
    compass() 
