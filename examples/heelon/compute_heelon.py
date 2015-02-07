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
Example for testing heel_on computation using a IMU Fox
"""
import numpy as np
import matplotlib.pyplot as plt
from sensbiotk.io import iofox_deprec as fox


def compute_heelon():
    """ heel_on computation
    """
    # Read IMU data
    [ftime, acc_imu, mag_imu, gyr_imu] = \
        fox.load_foximu_csvfile("wlkimushankR.csv")

    time = ftime[:, 1]
    slidingwindowsize = 10
    # sampling at 100Hz
    puissance_norme_acc = np.zeros(np.size(time))
    seekfor_gyrzero = 0
    seekfor_acctresh = 0
    heelon = []

    acc_norm = np.sqrt(acc_imu[:, 0] * acc_imu[:, 0]
                       + acc_imu[:, 1] * acc_imu[:, 1]
                       + acc_imu[:, 2] * acc_imu[:, 2])

    gyr_imu = gyr_imu * 180 / np.pi

    for t in range(slidingwindowsize/2 + 1,
                   np.size(time) - slidingwindowsize/2):
        puissance_norme_acc[t] =  \
            np.var(acc_norm[t-slidingwindowsize/2:t+slidingwindowsize/2])
        if seekfor_gyrzero == 0:
            if -gyr_imu[t, 2] >= 50:
                seekfor_gyrzero = 1
        if seekfor_gyrzero == 1 and seekfor_acctresh == 0:
            if -gyr_imu[t, 2] <= 0:
                seekfor_acctresh = 1
        if seekfor_gyrzero == 1 and seekfor_acctresh == 1:
            if puissance_norme_acc[t] >= 20:
                heelon.append(t)
                seekfor_gyrzero = 0
                seekfor_acctresh = 0

    print np.size(heelon)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(time, puissance_norme_acc)
    plt.plot(time, acc_norm)
    plt.subplot(212)
    plt.plot(time, gyr_imu)

    plt.figure(2)
    plt.plot(time, puissance_norme_acc)
    plt.plot(time, -gyr_imu[:, 2])
    plt.plot(time[heelon], puissance_norme_acc[heelon], 'bo')

    plt.show()

    return


if __name__ == '__main__':
    compute_heelon()
