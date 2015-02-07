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
Calib algo for gyrometer sensors data
"""
import numpy as np

# pylint:disable= I0011, E1101
# E1101 no-member false positif


def offset_fit(data):
    """ Compute offset from a constant signal to fit with zero

    Parameters :
    ------------
    data : numpy array of float
           [vx vy vz] data sensor containing all the acquisition
           on three axis

    Returns
    -------
    offset :numpy array of float (dim=3)
     offset parameters

     Notes
     -----
     To allow a good fitting, it must be with no motion
    """
    offset = [- np.mean(data[:, 0]),
              - np.mean(data[:, 1]),
              - np.mean(data[:, 2])]

    return offset


def compute(data):
    """ Compute IMU gyrometer calibration parameters

    Parameters :
    ------------
    data_nomotion : numpy array of float
                 data sensor motionless containing all the acquisition
                 on three axis

    Returns
    -------
     scale  : numpy array of float (dim=3)
               scale parameters
     offset : numpy array of float (dim=3)
              offset parameter
    """
    scale = [[1, 0, 0],[0, 1, 0],[0, 0, 1]]
    offset = offset_fit(data)

    return offset, scale
