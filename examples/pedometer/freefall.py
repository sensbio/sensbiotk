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
Example of a fall detector
"""
import numpy as np  
import pylab as py
from numpy.ctypeslib import ndpointer
import ctypes as ct

_LIBPED = ct.cdll.LoadLibrary('obj/libPedometer.so')

_LIBPED.pedometer.restype = None
_LIBPED.pedometer.argtypes = \
    [ct.c_int, ndpointer(ndim=1, shape=(3)),
     ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.POINTER(ct.c_float)]


def compute_ped(k, sig):
    """ compute pedometer
    """
    nbstep = ct.c_int()
    state  = ct.c_int()
    debug  = ct.c_float()
    _LIBPED.pedometer(k, sig, ct.byref(nbstep), ct.byref(state),
                      ct.byref(debug))
    return nbstep.value, state.value, debug.value


def test_cfreefall():
    """ Test pedometer implemented in C

    Returns
    -------
    status: str
          "OK" or "ERROR"
    """

    from  sensbiotk.io import iofox

    [timea, acc] = \
        iofox.load_foxacc_csvfile(".data/freefall1_acc.csv")

    val_state = np.zeros(len(acc))
    val_debug = np.zeros(len(acc))

    for k in range(0, len(acc)):
        tab = np.array(acc[k, 0:3],  dtype='f')
        [step, val_state[k], val_debug[k] ] = compute_ped(k, tab )

    py.figure()
    py.title("FreeFall Accelerations")
    py.plot(timea[:, 0], acc)
    py.figure()
    py.title("FreeFall detection Results (C)") 
    py.plot(val_state)

    return

def threshold_time(sig_time, sig_state, threshold_time):
     
    lensig = len(sig_state)
    sig_state_filt = np.zeros(lensig)

    # Initialisation
    index_start = 0
    sig_state_old = sig_state[0]

    for i in range(0, lensig):
        sig_state_filt[i] = sig_state[i]
        if  (sig_state[i] > 0) and ( sig_state[i]  != sig_state_old ):
            index_start = i
        else:
            if sig_state[i]  != sig_state_old :
                if (sig_time[i] - sig_time[index_start]) < threshold_time :
                    for j in range(index_start, i):
                        sig_state_filt[j] = 0

        sig_state_old = sig_state[i]
            

    return [sig_state_filt]


def threshold_sup(sig_raw, threshold, threshold_time = 0):
 
    lensig = len(sig_raw)
    sig_state = np.zeros(lensig)

    for i in range(0, lensig):
        if  (sig_raw[i] >= threshold):
            sig_state[i] = 1
        else:
            sig_state[i] = 0

    return [sig_state]


def threshold_inf(sig_raw, threshold, threshold_time = 0):
 
    lensig = len(sig_raw)
    sig_state = np.zeros(lensig)

    for i in range(0, lensig):
        if  (sig_raw[i] <= threshold):
            sig_state[i] = 1
        else:
            sig_state[i] = 0

    return [sig_state]


def search_state(sig_time, sig_raw, level, epsilon):
    """ Search stable state in signal

    Parameters :
    ------------
    sig_time: numpy array of float of dim N
     signal time
    sig_raw : numpy array of float of dim N
     signal input
    level : float
     level of the state signal
    epsilon : float
     delta precision around the level

    Returns
    -------
    sig_state: numpy array of int
     signal state detection : 1 level state, 0 outside level state
    """

    lensig = len(sig_raw)
    sig_state = np.zeros(lensig)

    for i in range(0, lensig):
        if  (sig_raw[i] <= level + epsilon) and \
            (sig_raw[i] >= level - epsilon) :
            sig_state[i] = 1
        else:
            sig_state[i] = 0


    return [sig_state]


def test_freefall():
    """ Test freefall detector implemented in Python

    Returns
    -------
    status: str
          "OK" or "ERROR"
    """

    from  sensbiotk.io import iofox
    from  sensbiotk.algorithms import basic as algo

    [timea, acc] = iofox.load_foxacc_csvfile("./data/freefall1_acc.csv")
    acc_norm = algo.compute_norm(acc)
    [state_freefall] =  threshold_inf(acc_norm, 1.5)
    [state_freefall] =  threshold_time(timea[:, 0], state_freefall, 0.1)

    [state_inactive] =  search_state(timea[:, 0], acc_norm, 10.0, 5.0)
    [state_inactive] =  threshold_time(timea[:, 0], state_inactive, 0.1)

    py.figure()
    py.plot(timea[:, 0], acc[:, 0:3])
    py.title("FreeFall Accelerations")
    py.legend(('x', 'y', 'z'), bbox_to_anchor=(0, 1, 1, 0),
              ncol=2, loc=3, borderaxespad=0.)

    py.figure()
    py.title("FreeFall detection Results (Python)")
    py.plot(acc_norm) 
    py.plot(state_freefall)
    py.plot(state_inactive*5) 

    return "OK"


if __name__ == '__main__':
    test_freefall()
    test_cfreefall()
    py.show()

