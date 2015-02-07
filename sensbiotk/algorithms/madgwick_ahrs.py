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
This algorithms is based on the work of Sebastian Madgwick described in :

Madgwick, Estimation of IMU and MARG orientation using a gradient descent
algorithm. 2011 Ieee International Conference on
Rehabilitation Robotics (Icorr), 2011.

It has been implemented in Python from the original Matlab author code.

It enables the computation of a quaternion from magneto-inertial measurements.

"""


import numpy as np
import math
from sensbiotk.transforms3d import quaternions as nq

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

def norm(x):
    """
    Computes the norm of x
    """
#    print "norm:", x
    tmpnorm = 0
    for i in range(0, len(x)):
        tmpnorm = tmpnorm + x[i]**2
    return math.sqrt(tmpnorm)

def update(q, z, fs=200):
    """
    Updates the computed q quaternion
    """

    accelero = z[0:3]
    magneto = z[3:6]
    gyro = z[6:9]

    sample_period = 1./fs
    Beta = 0.02

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
#    h = [1, 1, 1, 1]
    b = np.array([0, np.linalg.norm([h[1], h[2]]), 0, h[3]])
    # Gradient decent algorithm corrective step
    F = np.array([[2*(q[1]*q[3] - q[0]*q[2]) - accelero[0]],
           [2*(q[0]*q[1] + q[2]*q[3]) - accelero[1]],
          [2*(0.5 - q[1]**2 - q[2]**2) - accelero[2]],
          [2*b[1]*(0.5 - q[2]**2 - q[3]**2)
              + 2*b[3]*(q[1]*q[3] - q[0]*q[2]) - magneto[0]],
           [2*b[1]*(q[1]*q[2] - q[0]*q[3])
              + 2*b[3]*(q[0]*q[1] + q[2]*q[3]) - magneto[1]],
           [2*b[1]*(q[0]*q[2] + q[1]*q[3])
              + 2*b[3]*(0.5 - q[1]**2 - q[2]**2) - magneto[2]]])

    J = np.array([[-2*q[2], 2*q[3], -2*q[0], 2*q[1]],
         [2*q[1], 2*q[0], 2*q[3], 2*q[2]],
         [0, -4*q[1], -4*q[2], 0],
         [-2*b[3]*q[2], 2*b[3]*q[3],
           4*b[1]*q[2]-2*b[3]*q[0], -4*b[1]*q[3]+2*b[3]*q[1]],
          [-2*b[1]*q[3]+2*b[3]*q[1], 2*b[1]*q[2]+2*b[3]*q[0],
            2*b[1]*q[1]+2*b[3]*q[3], -2*b[1]*q[0]+2*b[3]*q[2]],
          [2*b[1]*q[2], 2*b[1]*q[3]-4*b[3]*q[1], 2*b[1]*q[0]-4*b[3]*q[2],
           2*b[1]*q[1]]])


    step = (np.dot(np.transpose(J), F))
    # normalise step magnitude
    step = step / norm(step)

    # Compute rate of change of quaternion
    q_dot = np.dot(
    0.5, nq.mult(q, (0, gyro[0], gyro[1], gyro[2]))) - \
    np.dot(Beta, np.transpose(step))

    # Integrate to yield quaternion
    q = q + (q_dot* sample_period)

    return q / np.linalg.norm(q)


