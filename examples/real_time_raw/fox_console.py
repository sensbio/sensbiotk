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
Fox dongle use with console
"""

import time
import logging
import sensbiotk.driver.fox_dongle as fox_dongle
from sensbiotk.io import iofox as fox

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
    foxdongle = fox_dongle.FoxDongle()

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

    # instanciate dongle
    foxdongle = fox_dongle.FoxDongle()

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
