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
Fast Quaternion Attitude Estimation from Accelerometer and Magnetometers
"""

# Not tested.
# See and transpose :
# sensbio/SensbioTk/SingleSensorMoCapAlgorithm/Markley/Test.py

import numpy as np

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103


def compute(z, a=np.array([0.5, 0.5])):
    """ Fast Quaternion Attitude Estimation from Accelerometer
    and Magnetometers 3D measures.

    See Publication : Fast Quaternion Attitude Estimation from
    Two Vector Measurements, L. Markley, NASA Tech Doc, 2001
    https://archive.org/details/nasa_techdoc_20010068636

    Parameters :
    ------------
    z  : numpy array of float (dim 6)
                 measurement vector containing 6 values:
                 3 accelerometer values and 3 magnetometer values
                 on one axis
    a: weighting parameter containing 2 values which should be most (dim 2)
                 of the time [0.5, 0.5]

    Returns
    -------
    q : numpy array of float (dim 4)
                attitude quaternion
    """

    # Gravity vector reference in inertial frame
    G = np.array([0, 1, 0], dtype=float)
    # Magnetometer vector reference in inertial frame
    H = np.array([0, 0.866, -0.5], dtype=float)
    # Normalized cross-product
    v3 = np.cross(G, H)
    r3 = v3/np.sqrt((v3**2).sum())

    g = z[0:3]
    h = z[3:6]

    a1 = a[0]
    a2 = a[1]

    # Normalized cross-product
    v3 = np.cross(g, h)
    b3 = v3/np.sqrt((v3**2).sum())

    isave = 0
    maxsave = np.dot(b3, r3)
    for i in range(1, 4):
        if maxsave < b3[i-1]*r3[i-1]:
            isave = i
            maxsave = b3[i-1]*r3[i-1]

    if isave:
        index = [ind for ind in range(0, 3) if ind != isave-1]
        r3[index] = -r3[index]
        G[index] = -G[index]
        H[index] = -H[index]

    alpha = (1 + np.dot(b3, r3))*(a1*np.dot(g, G) + a2*np.dot(h, H))\
        + np.dot(np.cross(b3, r3), (a1*np.cross(g, G) + a2*np.cross(h, H)))
    beta = np.dot((b3 + r3), (a1*np.cross(g, G) + a2*np.cross(h, H)))
    gamma = np.sqrt(alpha**2 + beta**2)

    if alpha > 0:
        k = 1/(2*np.sqrt(gamma*(gamma + alpha)*(1 + np.dot(b3, r3))))
        qopt0 = k*((gamma + alpha)*(1 + np.dot(b3, r3)))
        qoptv = k*((gamma + alpha)*(np.cross(b3, r3)) + beta*(b3 + r3))
    else:
        k = 1/(2*np.sqrt(gamma*(gamma - alpha)*(1 + np.dot(b3, r3))))
        qopt0 = k*((beta)*(1 + np.dot(b3, r3)))
        qoptv = k*((beta)*(np.cross(b3, r3)) + (gamma - alpha)*(b3 + r3))

    #the quaternion is rotated in the initial coordinate frame
    if isave == 1:
        q = np.concatenate([np.array([-qoptv[0]]), np.array([qopt0]),
                            np.array([-qoptv[2]]), np.array([qoptv[1]])])
    elif isave == 2:
        q = np.concatenate([np.array([-qoptv[1]]), np.array([qoptv[2]]),
                            np.array([qopt0]), np.array([-qoptv[0]])])
    elif isave == 3:
        q = np.concatenate([np.array([-qoptv[2]]), np.array([-qoptv[1]]),
                            np.array([qoptv[0]]), np.array([qopt0])])
    else:
        q = np.concatenate([np.array([qopt0]), qoptv])

    return q
