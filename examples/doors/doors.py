# -*- coding: utf-8; -*-
# This file is a part of sensbiotk
# Contact : sensbio@inria.fr
# Copyright (C) 2015  INRIA (Contact: sensbiotk@inria.fr)
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
Script for testing doors state using a IMU Fox
"""
import numpy as np
import matplotlib.pyplot as plt
from sensbiotk.io import iofox_deprec as fox
from sensbiotk.io import viz

# disabling pylint errors 'E1101' no-member, false positive from pylint
# pylint:disable=I0011,E1101

DIR = "./data"


def moving_average(data, fen):
    """ Moving Average on a signal

    Parameters :
    ------------
    data : numpy array of float of dim N
    signal to be filtered
    fen  : size of the windows for the moving average

    Returns
    -------
    V : numpy array of float
    signal filtered
    """
    win = np.ones(fen, 'd')
    dataf = np.convolve(win/win.sum(), data, mode='same')

    return dataf[fen-1:-fen+1]


def state_detection(time_imu, data, valopen, valclose, valeps):
    """ Compute three states door

    Parameters :
    ------------
    data : numpy array of float
           magnetometers norm of the IMU signals
    valopen: float
          magnetometers norm value for open door
    valclose: float
          magnetometers norm value for close door
     valeps: float
          epsilon magnetometers norm value to consider stable state

    Returns
    -------
    door_state: numpy array of float
                * door closed = 0
                * door opened = 1.0
                * door between this two state = 0.5
    """
    door_state = np.ones(len(data))
    door_event = []

    door_state_prev = -1
    for i in range(0, len(data)):
        # Compute the 'continuous' door_state
        if (data[i] <= valopen+valeps) and (data[i] >= valopen-valeps):
            door_state[i] = 1.0
        elif (data[i] <= valclose+valeps) and (data[i] >= valclose-valeps):
            door_state[i] = 0
        else:
            door_state[i] = 0.5
        # Note the door_state changement in door_event
        if door_state[i] != door_state_prev:
            print "door_event", time_imu[i], door_state[i]
        # Memorise the previous door_state for the next time
        door_state_prev = door_state[i]

    return [door_state, door_event]


def peak_detection(data, valplus):
    """ Compute three states door

    Parameters :
    ------------
    data : numpy array of float
           derivative magnetometers norm of the IMU signals
    valplus: float
          magnetometers norm value for open door
    valmoins: float
          magnetometers norm value for close door

    Returns
    -------
    door_state: numpy array of float
                * door closed = 0
                * door opened = 1.0
                * door between this two state = 0.5
    """
    door_state = np.ones(len(data))

    for i in range(0, len(data)):
        if data[i] >= valplus:
            door_state[i] = 1.0
        elif data[i] <= valplus:
            door_state[i] = 0.5
        else:
            door_state[i] = 0
    return door_state


def imu_door_norm(filename):
    """ Visualize the IMU signals, compute their norms,
    and give the extremun magnetometers norm

    Parameters
    ----------
    filename : filename IMU door to be analyzed
    time_i   : begin time of the extremun research
    time_f   : end time of the extremun research

    Returns
    -------
     [data
    """

    # Read IMU data
    [time, acc_imu, mag_imu, gyr_imu] = fox.load_foximu_csvfile(filename)
    time_imu = time[:, 1]
    # Sensors norm
    acc_norm = np.sqrt(np.sum(acc_imu[:, i]**2 for i in range(0, 3)))
    mag_norm = np.sqrt(np.sum(mag_imu[:, i]**2 for i in range(0, 3)))
    gyr_norm = np.sqrt(np.sum(gyr_imu[:, i]**2 for i in range(0, 3)))

    viz.plot_imu(1, "FOX IMU sensors", time_imu, acc_imu, mag_imu, gyr_imu)

    plt.figure(2)
    plt.subplot(311)
    plt.plot(time_imu, acc_norm)
    plt.title("FOX IMU norm signals sensors")
    plt.legend(('x', 'y', 'z'), bbox_to_anchor=(0, 1, 1, 0),
               ncol=2, loc=3, borderaxespad=0.)
    plt.ylabel('ACC (m/s^2)')
    plt.subplot(312)
    plt.plot(time_imu, mag_norm)
    plt.ylabel('MAG (gauss)')
    plt.subplot(313)
    plt.plot(time_imu, gyr_norm)
    plt.ylabel('GYR (rad/s)')
    plt.xlabel('time (s)')

    plt.figure(3)
    plt.title("FOX IMU samples verification")
    plt.plot(time_imu[1:], time[1:, 2])

    return[time_imu, acc_norm, mag_norm, gyr_norm]


def imu_door_mean(time_imu, mag_norm, time_i, time_f):
    """ Compute Mean on the window [time_i, time_f]
    """
   # id_i = np.where(time_imu >= time_i)
   # id_f = np.where(time_imu >= time_f)

    id_i = 0
    ltime = len(time_imu)
    while (time_imu[id_i] < time_i) and (id_i < ltime):
        id_i += 1

    id_f = 0
    while (time_imu[id_f] < time_f) and (id_f < ltime):
        id_f += 1

    return np.mean(mag_norm[id_i:id_f])


def imu_door_algo1(time_imu, mag_norm, gyr_norm, dimfen,
                   valopen, valclose, valeps):
    """ Test load_foximu_csvfile function

    Parameters
    ----------
    filename : filename IMU door to be analyzed
    """
    plt.figure(4)

    # Filter the mag norm
    mag_normfiltre = moving_average(mag_norm, dimfen)
    # State door computation
    [etat_porte, _ ]= \
        state_detection(time_imu, mag_normfiltre, valopen, valclose, valeps)
    # Plot the mag norm filtered and the door state
    plt.plot(time_imu[dimfen-1:-dimfen+1], mag_normfiltre)
    plt.plot(time_imu[dimfen-1:-dimfen+1], etat_porte)

    return


def test0():
    """ Test 0
    """
    filein = DIR + "HIGPS00.RAW"
    fileout = DIR + "imu00.csv"
    fileoutp = DIR + "presst00.csv"

    fox.convert_fox_rawfile(filein, fileout, fileoutp)
    [time, acc_imu, mag_imu, gyr_imu] = fox.load_foximu_csvfile(fileout)
    time_imu = time[:, 1]
    viz.plot_imu(1, "FOX IMU sensors", time_imu, acc_imu, mag_imu, gyr_imu)


def test1():
    """ Test 1
    """
    [time_imu, acc_norm, mag_norm, gyr_norm] = \
        imu_door_norm(DIR+"/output01_imu.csv")
    state_open = imu_door_mean(time_imu, mag_norm, 15.0, 20.0)
    state_close = imu_door_mean(time_imu, mag_norm, 25.0, 30.0)
    print state_open, state_close, np.abs(state_close - state_open)/3
    imu_door_algo1(time_imu, mag_norm, gyr_norm, 100, 1.21, 0.96, 0.05)
    return


def test2():
    """ Test2
    """
    #fox.convert_fox_rawfile("data/porte_01.RAW",
    #                   "data/bureau00_imu.csv","data/porte_01_presst.cvs")
    [time_imu, acc_norm, mag_norm, gyr_norm] = \
        imu_door_norm(DIR+"/porte_01_imu.csv")
    state_open = imu_door_mean(time_imu, mag_norm, 9.0, 10.0)
    state_close = imu_door_mean(time_imu, mag_norm, 15.0, 16.0)
    print state_open, state_close, np.abs(state_close - state_open)/3
    imu_door_algo1(time_imu, mag_norm, gyr_norm, 5, 0.45, 0.25, 0.05)
    return


def test3():
    """ Test3
    """

    cfg = [[DIR+"/maison00_imu.csv", 38.0, 42.0, 51.0, 53.0],
           [DIR+"/maison01_imu.csv", 10.0, 12.0, 20.5, 21.5],
           [DIR+"/maison02_imu.csv", 21.0, 22.0, 39.0, 41.0]]

    id_cfg = 2

    print "MANIP ", cfg[id_cfg][0]
    [time_imu, acc_norm, mag_norm, gyr_norm] = imu_door_norm(cfg[id_cfg][0])

    state_open = imu_door_mean(time_imu, mag_norm,
                               cfg[id_cfg][1], cfg[id_cfg][2])
    state_close = imu_door_mean(time_imu, mag_norm,
                                cfg[id_cfg][3], cfg[id_cfg][4])
    eps = np.abs(state_close - state_open)/3
    print "PARAM ", state_open, state_close, eps
    print "EVENTS "
    imu_door_algo1(time_imu, mag_norm, gyr_norm,
                   5, state_open, state_close, eps)

    return


def test4():
    """ Test4
    """
    cfg = [[DIR+"/bureau00_imu.csv", 10.0, 150.0, 27.0, 29.0],
           [DIR+"/bureau01_imu.csv", 10.0, 15.0, 25.0, 28.0],
           [DIR+"/bureau02_imu.csv", 13.0, 18.0, 25.0, 30.0],
           [DIR+"/bureau03_imu.csv", 13.0, 18.0, 25.0, 30.0],
           [DIR+"/bureau04_imu.csv", 13.0, 18.0, 25.0, 30.0]]

    id_cfg = 3

    print "MANIP ", cfg[id_cfg][0]
    [time_imu, acc_norm, mag_norm, gyr_norm] = imu_door_norm(cfg[id_cfg][0])

    state_open = imu_door_mean(time_imu, mag_norm,
                               cfg[id_cfg][1], cfg[id_cfg][2])
    state_close = imu_door_mean(time_imu, mag_norm,
                                cfg[id_cfg][3], cfg[id_cfg][4])
    eps = np.abs(state_close - state_open)/3
    print "PARAM ", state_open, state_close, eps
    print "EVENTS "
    imu_door_algo1(time_imu, mag_norm, gyr_norm,
                   5, state_open, state_close, eps)

    return

if __name__ == '__main__':
    test4()
    plt.show()
