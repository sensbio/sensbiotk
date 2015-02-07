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
Example of a pedometer
"""
import numpy as np
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

def test_cpedometer():
    """ Test pedometer implemented in C

    Returns
    -------
    status: str
          "OK" or "ERROR"
    """

    from  sensbiotk.io import iofox
    import pylab as py

    [timea, acc] = \
        iofox.load_foxacc_csvfile("./data/walk4_acc.csv")
   # [timea, acc] = cut_signal(timea, acc, 12.0, 29.0)

    peak_detected = np.zeros(len(acc))

    for k in range(0, len(acc)): 
        tab = np.array(acc[k, 0:3],  dtype='f')
        [step, state, peak_detected[k]]  = compute_ped(k, tab)

    print "Step numbers=", step

    py.figure()
    py.plot(timea[:, 0], acc)
    py.figure()
    #py.plot(peak_detected, "o")
    py.show()


def test_pedometer():
    """ Test pedometer implemented in Python

    Returns
    -------
    status: str
          "OK" or "ERROR"
    """

    from  sensbiotk.io import iofox
    from  sensbiotk.algorithms import basic as algo
    import pylab as py

    [timea, acc] = iofox.load_foxacc_csvfile("./data/walk1_acc.csv")
    [timea, acc] = algo.cut_signal(timea, acc, 12.0, 29.0)
    acc_norm = algo.compute_norm(acc)
    #acc_filt = algo.lowpass_filter(acc_norm, 2.0, 100.0)
    #acc_filt = algo.lowpass_filter2(acc_norm, 2.0, 200.0)
    acc_filt = algo.moving_average(acc_norm, 30)
    #acc_filt = algo.moving_average2(acc_norm, 50)
    index_peak = algo.search_maxpeak(acc_filt)
    [time_peak, acc_peak] = algo.threshold_signal(timea[index_peak],
                                                  acc_filt[index_peak], 11.0)
    print "Step numbers=", len(acc_peak)

    py.figure()
    py.plot(timea[:, 0], acc[:, 0:3])
    py.title("Walking 1 Accelerations")
    py.legend(('x', 'y', 'z'), bbox_to_anchor=(0, 1, 1, 0),
              ncol=2, loc=3, borderaxespad=0.)

    py.figure()
    py.title("Walking 1 Results")
    py.plot(timea[:, 0], acc_norm)
    py.plot(timea[:, 0], acc_filt)
    py.plot(time_peak, acc_peak, "o")

    py.figure()
    py.plot(np.diff(acc_filt))
    py.plot(np.diff(np.sign(np.diff(acc_filt)) < 0))
    py.show()

    return "OK"


if __name__ == '__main__':
    #test_cpedometer()
    test_pedometer()
