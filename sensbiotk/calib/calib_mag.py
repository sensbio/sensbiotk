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
Calib algo for magnetometers sensors data
"""
import numpy as np

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

SEP = ";"


def unit_sphere_fit(data):
    """ Calibration using Unit Sphere Fitting algo.

    Parameters :
    ------------
    data : numpy array of float of dim N
    data sensor containing all the acquisition for the different axes

    Returns
    -------
    scale :numpy array of float
     scale parameters
    offset :numpy array of float
     offset parameters

     Notes
     -----
     To allow a good fitting, the motion must cover all axis
     rotation without high acceleration.
    """

    # Normalization step
    mins = np.array([np.min(data[:, 0]),
                     np.min(data[:, 1]), np.min(data[:, 2])])
    maxs = np.array([np.max(data[:, 0]),
                     np.max(data[:, 1]), np.max(data[:, 2])])

    scale1 = 2.0 / (maxs - mins)
    offset1 = (maxs + mins) / 2
    data = (data - offset1) * scale1

    # Start sphere fitting method
    data_stat = np.concatenate((data*data, 2*data), axis=1)
    if 1 / (np.linalg.cond(np.dot(data_stat.transpose(), data_stat), 1)) \
            > 1e-7:
        param = np.dot(np.sum(data_stat, axis=0).reshape(1, 6),
                       np.linalg.inv(np.dot(data_stat.transpose(), data_stat)))
        ratio = 1 + \
            np.sum((param[0, 3:6] * param[0, 3:6]) / param[0, 0:3])
        scale2 = np.sqrt(param[0, 0:3] / ratio)
        offset2 = -param[0, 3:6] / param[0, 0:3]
    else:
        scale2 = np.ones([1, 3])
        offset2 = np.zeros([1, 3])

    offset = offset1 + offset2 / scale1
    scale = scale1 * scale2

    return offset, scale


def compute(data):
    """ Compute IMU magnetometer calibration parameters

    Parameters :
    ------------
    data : numpy array of float
           data sensor in motion containing all the acquisition
           on three axis

    Returns
    -------
     scale  : numpy array of float (dim=3)
               scale parameters
     offset : numpy array of float (dim=3)
              offset parameter
    """

    offset, scale1 = unit_sphere_fit(data)

    scale = np.array([[scale1[0], 0.0, 0.0], [0.0, scale1[1], 0.0],
                      [0.0, 0.0, scale1[2]]])

    return offset, scale
