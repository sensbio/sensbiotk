 
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 19:06:44 2015

@author: bsijober
"""

import time
import BaseHTTPServer
import numpy as np
from sensbiotk.driver import fox_dongle as fdongle
from sensbiotk.transforms3d.eulerangles import quat2euler
from sensbiotk.transforms3d import quaternions as nq
import sensbiotk.algorithms.martin_ahrs as martin
from sensbiotk.calib import calib_mag
from threading import Thread

HOST_NAME = 'localhost' 
PORT_NUMBER = 8000 


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response()
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        if str(s.path) == '?request=init':
            rt.init_frame()
        quat = rt.quaternion
        euler = rt.euler
        s.wfile.write(str(euler[2]*180/np.pi) +' '+str(euler[1]*180/np.pi) +' '+
        str(euler[0]*180/np.pi) +' '+ str(quat[0]) +' '+ str(quat[1]) +' '+
        str(quat[2]) +' '+ str(quat[3]))
        
                
            
        
class RT_Martin():
    def __init__(self):
        """Class Initialization"""

        self.rot_x_offset = 0
        self.rot_y_offset = 0
        self.rot_z_offset = 0    
        
        self.scale = np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
        self.offset = np.array([0, 0, 0])
          
         # booleans def
        self.init = False
        self.calib_mag_bool = False
        self.init_obs = False
        self.init_frame_bool = False

        self.quat_offset = [1, 0, 0, 0] #the quat transformation from NEDown frame to the original one

        self.observer = martin.martin_ahrs()

        self.euler = np.array([0, 0, 0]) 
        
        return

    def init_imu(self):
        while not self.init:
            # handle dongle initialization
            if foxdongle.init_dongle():
                self.init = True
                print 'Device is connected to %s.' % (foxdongle.line())
                
    def calib_magneto(self):
        print '---- Magnetometer Calibration ---- '
        while not self.calib_mag_bool:
            if foxdongle.is_running():
                data = foxdongle.read()
                if data is not None and data.shape == (11,):
                    print 'Calib magneto, 20 seconds \n'
                    data_calib = np.zeros((4000,11))
                    for i in range(1,4000):
                        data_calib[i] = foxdongle.read().reshape(1, 11)
                        time.sleep(0.005)
                    self.offset, self.scale = calib_mag.compute(data_calib[:,5:8])
                    print self.scale
                    print self.offset
                    print '---- Calib Magneto Over ----'
                    self.calib_mag_bool = True

    def update(self, data):

        self.quaternion = nq.mult(self.quat_offset, self.observer.update(data[0, 2:12], 0.010))
        self.euler = np.array(quat2euler(self.quaternion))

        print 'Quaternion : ' + str(self.quaternion) +'\n' + 'Rz : '+'%0.2f' %((self.euler[0])*180/np.pi)+' '+u'°' +\
        ' Ry : '+'%0.2f' %((self.euler[1])*180/np.pi)+' '+u'°' + ' Rx : '+'%0.2f' %((self.euler[2])*180/np.pi)+' '+u'°'

    def init_observer(self):
        print '---- Initializing the observer... ----'
        print '-- Please stay without moving in the initial position --'           
        while not self.init_obs:
            if foxdongle.is_running():
                data = foxdongle.read()
                if len(data) != 0: 
                        time.sleep(4)
                        data_obs = np.zeros((1000, 11))
                        for i in range(0,1000):
                            data = foxdongle.read().reshape(1, 11)
                            data[0, 5:8] = np.transpose(np.dot(self.scale,np.transpose((data[0, 5:8]-np.transpose(self.offset)))))
                            data_obs[i,:] = data[:]
                            time.sleep(0.005)
                            print('.'),
                        self.init_obs = True
        data_init = np.mean(data_obs[:,2:12],0)
        self.quaternion = self.observer.init_observer(data_init[2:8])

    def init_frame(self):
        self.quat_offset = nq.conjugate(self.quaternion)
        print('!!!!!!!!!!!!!!!!!!!!! GROS PRINT !!!!!!!!!!!!!!!!!!!!!!!!!!')
#        self.init_frame_bool = True

    def thread_data(self):
        if foxdongle.is_running():
            data = foxdongle.read()
            if data is not None and data.shape == (11,):
                data = data.reshape(1,11)
                data[0, 5:8] = np.transpose(np.dot(rt.scale,np.transpose((data[0, 5:8]-np.transpose(rt.offset)))))
                rt.update(data)
                

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)

    # inits RT_Martin class
    rt = RT_Martin()
    # instanciates dongle
    foxdongle = fdongle.FoxDongle() 
    # connects dongle
    rt.init_imu()
    # calib magneto
    rt.calib_magneto()
    # init observer
    rt.init_observer()
    # init frame
    rt.init_frame()                 
    #init thread for reading/updating data
    t = Thread(target=rt.thread_data, args=())
    t.start()
    
    # inits server
    try:
        httpd.serve_forever()
        
                    
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)