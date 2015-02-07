# -*- coding: utf-8 -*-
"""
This example uses the real-time FOX library combined to mahony ahrs algorithm for 
computing the quaternions and visualizing them in 3D.

@author: bsijober
"""

from sensbiotk.driver import fox_dongle as fdongle
import time
import numpy as np
import logging
from sensbiotk.transforms3d.eulerangles import quat2euler
from sensbiotk.transforms3d.quaternions import quat2mat
from visual import *
import sensbiotk.algorithms.mahony_ahrs as mahony
from sensbiotk.calib import calib_mag

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

class RT_Mahony():
    
    def __init__(self):
        """Class Initialization"""
        self.IMU = 0
        self.rot_x_display = 0
        self.rot_y_display = 0
        self.rot_z_display = 0
        
        self.rot_x_offset = 0
        self.rot_y_offset = 0
        self.rot_z_offset = 0
        
        return

    def acq_callback(obj):
        """ callback"""
        print "Nb of sample", len(obj.data)
#        update(obj)
     
    def f_3D_plot_init(self):
        
         #######################
         # 3D objects init
         #######################
    
        scene.title = "VISU QUATERNION"
        scene.autocenter = False
        scene.scale = (0.05,0.05,0.05)
        scene.background = (255, 255, 255)
        scene.width = 900
        scene.height = 600
        scene.forward = (0, 0, 1)
#        scene.up = (0, 1, 0)
    
        x_frame = arrow(pos=(0,0,0), axis=(-10, 0, 0), shaftwidth=1, color=color.blue)
        y_frame = arrow(pos=(0,0,0), axis=(0, 10, 0), shaftwidth=1, color=color.green)
        z_frame = arrow(pos=(0,0,0), axis=(0, 0, 10), shaftwidth=1, color=color.red)
        
        self.IMU = box(pos=(0, 0, 0), axis = (8, 0, 0), height = 5, width = 3, color = color.black, length = 8)
        self.text = text(text='HikoB', pos=(3.2,-1,0), depth=2, color=color.white, height = 1.8, axis =(-1,0,0))
        
        self.rot_x_display = label(text='X Rotation : 0 '+u'°', yoffset=0, xoffset=0, line=False, box=False, color=color.blue, height=18, pos=(-14, 0, 0))
        self.rot_y_display = label(text='Y Rotation : 0 '+u'°', yoffset=0, xoffset=0, line=False, box=False, color=color.green, height=18, pos=(0, 11, 0))
        self.rot_z_display = label(text='Z Rotation : 0 '+u'°', yoffset=0, xoffset=0, line=False, box=False, color=color.red, height=18, pos=(5, 2, -14))
                
        self.euler = np.array([0, 0, 0])
        self.quaternion = np.array([1, 0, 0, 0])
        
    def update(self, data):
        
        [self.quaternion] = np.array(mahony.update(self.quaternion, data))
        self.euler = np.array(quat2euler(self.quaternion))
        
        print 'Quaternion : ' + str(self.quaternion) +'\n' + 'Rz : '+'%0.2f' %((self.euler[0])*180/pi)+' '+u'°' +\
        ' Ry : '+'%0.2f' %((self.euler[1])*180/pi)+' '+u'°' + ' Rx : '+'%0.2f' %((self.euler[2])*180/pi)+' '+u'°'


        # Rotation along z
        self.rot_z_display.text = 'Z Rotation : '+'%0.2f' %((self.euler[0])*180/pi)+' '+u'°'
        # Rotation along y
        self.rot_y_display.text = 'Y Rotation : '+'%0.2f' %((self.euler[1])*180/pi)+' '+u'°'       
        # Rotation along x
        self.rot_x_display.text = 'X Rotation : '+'%0.2f' %((self.euler[2])*180/pi)+' '+u'°'
        
        # Put the IMU in its original position
        self.IMU.axis = (8, 0, 0)
        self.IMU.up = (1, 0, 0)
        # Rotate it of arccos(qw)*2 on the axis qx,qy,qz
        self.IMU.rotate(origin=(0, 0, 0), angle=np.arccos(self.quaternion[0])*2, axis=(self.quaternion[1:4]))
#        print(self.quaternion[1:4])
        
    
        
    
def real_time_mahony():
        
        
        rt = RT_Mahony()
        
        # instanciate dongle
        foxdongle = fdongle.FoxDongle()
    
        # init 3d visu
        rt.f_3D_plot_init()
        
        print 'Enter acquisition loop (type ^C to stop).'
    
        init = False
        calib_mag_bool = False  
        
        scale = np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
        offset = np.array([0, 0, 0])
        
        while True:
            try:
                # handle dongle initialization
                if not init and foxdongle.init_dongle():
                    init = True
                    print 'Device is connected to %s.' % (foxdongle.line())
                if foxdongle.is_running():
                    data = foxdongle.read()
                    if data is not None and data.shape == (11,):                    
                        data.reshape(1,11)
                        data[5:8] = np.transpose(np.dot(scale,np.transpose((data[5:8]-np.transpose(offset)))))
                        if not calib_mag_bool: # record 40s of data for the magnetometer calibration
                            print 'Calib magneto, 20 seconds \n'
                            data_calib = np.zeros((4000,11))
                            for i in range(1,4000):
                                    data_calib[i] = foxdongle.read().reshape(1, 11)
                                    time.sleep(0.005)
                            offset, scale = calib_mag.compute(data_calib[:,5:8])
                            print scale
                            print offset
                            print 'Calib magneto over'
                            print '-----------------\n'
                            print 'Hold the IMU as on the VPython visualization (initial position)'
                            time.sleep(6)
                            print 'START'
                            rt.text.height = 0 
                            calib_mag_bool = True
                        else:
                            rt.update(data[2:12])
                    time.sleep(0.005)
                
        
            except KeyboardInterrupt:
                print "\nStopped"
                break
            except Exception as e:
                logging.error('exception reached:' + str(e))
               
    
        # must close to kill read thread (fox_sink)
        foxdongle.close_dongle()
               
    
        print 'Done'

if __name__ == '__main__':
   real_time_mahony()
