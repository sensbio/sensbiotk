# -*- coding: utf-8 -*-
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
Computes rotation angle between two quaternions

@author: bsijober
"""

import numpy as np
from sensbiotk.transforms3d import quaternions as nq

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

def compute(q_0, q_1, q_offset=[1, 0, 0, 0]):

    """ Computes rotation angle between two quaternions

    Parameters :
    ------------
    q_0  : numpy array of float
                 the first quaternion (w, x, y, z)
    q_1 : numpy array of float
                 the second quaternion (w, x, y, z)
    q_offset : numpy array of float
                 the initial quaternion corresponding to the offset
                 between q_0 and q_1 at an initial position
                 (can be generated using sensbiotk.calib.calib_geom)

    Returns
    -------
     angle : float
             the angle of rotation between q_0 and q_1 (rad)
     rot_axis : numpy array of float
             the axis of rotation

    """

    q_corr = nq.mult(
        nq.mult(np.transpose(nq.conjugate(q_0)),
                np.transpose(q_1)), nq.conjugate(
                q_offset)) # q_corr = conj(q_0) x q_1 x conj(q_offset)
    angle = np.arccos(q_corr[0])*2 # angle = acos(q_corr(w)) x 2
    rot_axis = q_corr[1:4] # the axis of rotation between
    # the two quaternions (ex: if along Z, should be close to [0, 0, 1])

    return angle, rot_axis

