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
This algorithms is based on the work of Robert Mahony described in :

Mahony, R., T. Hamel, and J.-M. Pflimlin, Nonlinear Complementary Filters
on the Special Orthogonal Group. Automatic Control,
IEEE Transactions on, 2008. 53(5): p. 1203-1218.

It enables the computation of a quaternion from magneto-inertial measurements.

"""


import numpy as np
import math
from sensbiotk.transforms3d import quaternions as nq

# disabling pylint errors 'E1101' no-member, false positive from pylint
# pylint:disable=I0011,E1101

class obj:
    eInt = 0

def norm(x):
#    print "norm:", x
    tmpnorm = 0
    for i in range(0, len(x)):
        tmpnorm = tmpnorm + x[i]**2
    return math.sqrt(tmpnorm)

def update(q, z, fs=200):

    accelero = z[0:3]
    magneto = z[3:6]
    gyro = z[6:9]

    sample_period = 1./fs
    Kp = 0.01 # algorithm proportional gain
    Ki = 0 # algorithm integral gain

    # Normalise accelerometer measurement
    norm_accelero = norm(accelero)
    if  norm_accelero != 0:
        accelero = accelero / norm_accelero
    # Normalise magnetometer measurement
    norm_magneto = norm(magneto)
    if  norm_magneto != 0:
        magneto = magneto / norm_magneto
    # Reference direction of Earth's magnetic field
    h = nq.mult(q, nq.mult(np.concatenate(([0], magneto)), nq.conjugate(q)))
    b = np.array([0, np.linalg.norm([h[1], h[2]]), 0, h[3]])

    # Estimated direction of gravity and magnetic field
    v = np.array([[2*(q[1]*q[3] - q[0]*q[2])],
         [2*(q[0]*q[1] + q[2]*q[3])],
         [q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2]])
    w = np.array(
    [[2*b[1]*(0.5 - q[2]**2 - q[3]**2) + 2*b[3]*(q[1]*q[3] - q[0]*q[2])],
         [2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3])],
         [2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]**2 - q[2]**2)]])

    # Error is sum of cross product between
    # estimated direction and measured direction of fields
    e = np.cross(np.transpose(accelero),
                 np.transpose(v)) + np.cross(
                 np.transpose(magneto), np.transpose(w))

    if(Ki > 0):
        obj.eInt = obj.eInt + e * sample_period

    # Apply feedback terms
    gyro = np.transpose(gyro + Kp * e + Ki * obj.eInt)

    # Compute rate of change of quaternion
    q_dot = np.dot(0.5, nq.mult(q, (0, gyro[0], gyro[1], gyro[2])))

    # Integrate to yield quaternion
    q = q + np.transpose((q_dot* sample_period))

    return q / np.linalg.norm(q)
