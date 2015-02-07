"""
Example for algorithms/basic/
"""

import numpy as np
import sensbiotk.algorithms.basic as algo

# pylint:disable= I0011, E1101
# E1101 no-member false positif


def example_static_period():
    """ Example: static period
    """
    from sensbiotk.io.uigetfile import uigetfile
    from sensbiotk.io.iofox import load_foxcsvfile
    import matplotlib.pyplot as plt

    # Load the recording with motionless periods
    # For example choose :
    # sensbiotk/tests/data/calib_accelerometer/IMU4/HKB0_02.csv
    filename =\
        uigetfile(
            title='Select the IMU .csv file',
            filetypes=[('.csv file', '.csv')])
    [time, _, _, _, _, _, _, _, _, gyrz] = \
        load_foxcsvfile(filename)

    # Load the recording with motionless periods
    freqs = 200
    start, end = algo.find_static_periods(gyrz, 2 * np.pi/180, 3*freqs)

    plt.hold(True)
    plt.plot(time, gyrz)
    for i in range(0, len(start)):
        plt.axvline(x=time[start][i], color='g')
        plt.axvline(x=time[end][i], color='r')

    plt.show()
    return


if __name__ == '__main__':
    example_static_period()
