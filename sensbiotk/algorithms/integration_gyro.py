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
# along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
Gyrometer integration signal
"""
from scipy import integrate
from scipy import signal
import numpy as np

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103


def compute(data, freqs=200):

    """ Compute a minimized drift integration of the gyrometer signal

    Parameters :
    ------------
    data  : numpy array of float
                 gyrometers data containing all the acquisition
                 on one axis
    Returns
    -------
    theta : numpy array of float
                the absolute angle in degree

    """
    # highpass filter for removing near-constant component
    [b, a] = signal.butter(1, 0.025/(freqs/2.), btype='high')
    data = signal.filtfilt(b, a, data, axis=0)
    # lowpass filter => white noise filtering
#    [b, a] = signal.butter(2, 20/(freqs/2.), btype='low')
#    data = signal.filtfilt(b, a, data, axis=0)
    # threshold filter
#    data[np.abs(data) < (0.3 * np.pi/180)] = 0
    theta = (integrate.cumtrapz(data, dx=1./freqs, axis=-1,
                                initial=0))*180/np.pi

    return theta
