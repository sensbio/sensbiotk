"""
Tests Unit for algorithms/basic
"""

import numpy as np
import sensbiotk.algorithms.basic as algo

from nose.tools import assert_equal

# pylint:disable= I0011, E1101
# E1101 no-member false positif


def test_static_period():
    """ Test: static period
    """
    from sensbiotk.io.uigetfile import uigetfile
    from sensbiotk.io.iofox import load_foxcsvfile

    # Load the recording with motionless periods
    [time, _, _, _, _, _, _, _, _, gyrz] = \
        load_foxcsvfile("data/calib_accelerometer/IMU4/HKB0_02.csv")
    freqs = 200
    resp = True
    start, end = algo.find_static_periods(gyrz, 2 * np.pi/180, 3*freqs)

    for i in range(0, len(start)):
        # The standard deviation of the gyrz signal must be small
        std_static = np.std(gyrz[range(start[i], end[i])])
        if std_static > 0.02:
            resp = False
    yield assert_equal, resp, True
