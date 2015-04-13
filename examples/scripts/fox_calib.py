#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is a part of sensbiotk
# Contact : sensbiotk@inria.fr
# Copyright (C) 2015  INRIA
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

# pylint:disable= I0011, E1101, R0912, R0913, R0914, R0915
# E1101 no-member false positif

"""
IMU sensors calibration
"""

import numpy as np
from sensbiotk.io.iofox import load_foxcsvfile
import sensbiotk.calib.calib as calib
import matplotlib.pyplot as plt

DATACALIBFILE = "data/calib01_imu.csv"
CALIBFILE= "data/calib_imu1.txt"

def calib_param( datacalibfile, calibfile, comments=""):
    """ Load or compute calibration parameters
    """
    [params_acc, params_mag, params_gyr] = \
        calib.compute(imuNumber=5 ,filepath=DATACALIBFILE, param = 3)
    calib.save_param(calibfile, 
                     params_acc, params_mag, params_gyr, comments)

    return [params_acc, params_mag, params_gyr]


def launch():
    """ run example : "martin"
    """
    # Compute (True) or load (False
    [params_acc, params_mag, params_gyr] = calib_param(DATACALIBFILE, CALIBFILE)
   

if __name__ == '__main__':
    launch() 
    plt.show()
