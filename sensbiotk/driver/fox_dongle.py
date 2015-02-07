# -*- coding: utf-8; -*-
# This file is a part of sensbiotk
# Contact : sensbio@inria.fr
# Copyright (C) 2014  INRIA (Contact: sensbiotk@inria.fr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Fox dongle management module
"""
import time
import logging
from threading import Lock
import numpy as np
import fox_sink


class FoxDongle():
    """ Class to manage Fox dongle data sensor reception """

    def __init__(self):
        """Class Initialization"""
        # sink node FoxSink class
        self.sinknode = None
        # user callback
        self.callback = None
        # PC time when the connection has been
        # established with the sink node
        self.time0 = 0.0
        # Sample time of acquisition in seconds
        self.sampletime = 1
        # Data list acquisition [time,ax,ay,az,mx,my,mz,gx,gygz] (storage)
        self.data = []
        # Mutex to handle 'data access' critical section (FRD)
        self.data_mutex = Lock()
        # Last Data value [time,nax,ay,az,mx,my,mz,gx,gy,gz]
        self.lastdata = [0, 0]

    def init_dongle(self, funcname = None):
        """ Search a Fox sink dongle on serial link

        Parameters :
        ------------
        funcname: fonction without return and parameters
            user callback function to be called during the data reception
        """

        # Reset data
        self.data = []
        self.lastdata = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Class fox_pedometer instantiation
        self.sinknode = fox_sink.FoxSink()

        logging.debug('Search USB serial line...')

        if self.sinknode.connect_serial() is False:
            logging.debug('Line not found')
            return False # failed

        logging.debug('Line found = ' + self.line())

        # PC time:time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.sinknode.fox_run()
        self.time0 = round(time.time())
        self.callback = funcname
        self.sinknode.set_callback(self.store)
        self.sinknode.start_read()

        return True # ok

    def close_dongle(self):
        """ Close the serial link of the Fox pedometer dongle
        """

        if not self.sinknode is None:
            self.sinknode.fox_close()
        return

    def is_running(self):
        """ Say if the Fox pedometer dongle 'read process' is running
        """
        return self.sinknode.run

    def line(self):
        """ Return the sinknode line value (string)
        """
        return str(self.sinknode.line)

    def read(self):
        """ Read the last stored data

        Returns :
        ---------
        onesample : [float, f, f, f, f, f, f, f, f, f]
        read/pop the last data value [time, datas]

        """

        self.data_mutex.acquire() # enter critical section
        if len(self.data) != 0:
            onesample = self.data[-1]
        else:
            onesample = None
        self.data_mutex.release() # leave critical section

        return onesample

    def unstack_read(self):
        """ Reads one data stored and erases it

        Returns :
        ---------
        onesample : [float, f, f, f, f, f, f, f, f, f]
        read/pop the last data value [time, datas]

        """

        self.data_mutex.acquire() # enter critical section
        if len(self.data) != 0:
            onesample = self.data[-1]
            np.delete(self.data, (-1), axis=0)
        else:
            onesample = None
        self.data_mutex.release() # leave critical section

        return onesample


    def read_all(self):
        """ Read one data stored

        Returns :
        ---------
        time : list of [float, int]
        read/pop the complete list ([t0, steps0],...,[t0, steps0])
        """

        self.data_mutex.acquire() # enter critical section
        copy_data = self.data
        self.data = []
        self.data_mutex.release() # leave critical section

        return copy_data

    def store(self):
        """ Fox sink read callback to store data
        """

        self.data_mutex.acquire() # enter critical section

        # handle sink node
        try:
           
            #onesample = [(self.sinknode.count * self.sampletime) + self.time0,
            #             self.sinknode.sensor]
            onesample = np.array([(self.sinknode.count * self.sampletime) + self.time0,
                                 self.sinknode.count,
                                 self.sinknode.sensor[0], self.sinknode.sensor[1],\
                                 self.sinknode.sensor[2],\
                                 self.sinknode.sensor[3], self.sinknode.sensor[4],\
                                 self.sinknode.sensor[5],\
                                 self.sinknode.sensor[6], self.sinknode.sensor[7],\
                                 self.sinknode.sensor[8]])
            
            if self.data == []:
                self.data = onesample
            else:
                self.data =  np.vstack((self.data, onesample))

            #self.data.append(onesample)
            self.lastdata = onesample # saved
            logging.debug('Store' + len(self.data) + onesample)

        except Exception as e:
             logging.debug('exception reached:' + str(e))

        self.data_mutex.release() # leave critical section

        # Launch the user callback
        try:
            if self.callback is not None:
                self.callback(self)
        except:
            logging('exception reached:' + str(e))

        return

##
## main test part
##

def test_acq_callback(obj):
    """ Fake function to test callback"""
    print "Nb of sample", len(obj.data)

def test1():
    """ Example of use of the Fox Sink dongle
    """
    # instanciate dongle
    foxdongle = FoxDongle()

    print 'Enter acquisition loop (type ^ to stop).'

    init = False
    while True:
        try:
            # handle dongle initialization
            if not init and foxdongle.init_dongle(test_acq_callback):
                init = True
                print 'Device is connected to %s.' % (foxdongle.line())

            if foxdongle.is_running():
                time.sleep(5)
                val = foxdongle.read_all()
                print "READ_ALL:", val
            elif init:
                init = False
                print 'Device is disconnected. Please reconnect.'

        except KeyboardInterrupt:
            print "\nStopped."
            break
        except Exception as e:
            logging.error('exception reached:' + str(e))

    # must close to kill read thread (fox_pedometer)
    foxdongle.close_dongle()

    print 'Done'


def test2():
    """ Example of use of the Fox Sink dongle
    """
    from sensbiotk.io import iofox as fox

    # instanciate dongle
    foxdongle = FoxDongle()

    print 'Enter acquisition loop (type ^C to stop and save tmp_imu.csv).'

    init = False
    while True:
        try:
            # handle dongle initialization
            if not init and foxdongle.init_dongle(test_acq_callback):
                init = True
                print 'Device is connected to %s.' % (foxdongle.line())
           
            time.sleep(5)
        except KeyboardInterrupt:
            print "\nStopped and Record in tmp_imu.csv."
            
            resp = fox.save_foxsignals_csvfile(foxdongle.data[:, 1], 
                                               foxdongle.data[:, 2:5],\
                                               foxdongle.data[:, 5:8],\
                                               foxdongle.data[:, 8:11],
                                               "tmp_imu.csv")
            break
        except Exception as e:
            logging.error('exception reached:' + str(e))
           

    # must close to kill read thread (fox_sink)
    foxdongle.close_dongle()
           

    print 'Done'

if __name__ == '__main__':
    test2()
