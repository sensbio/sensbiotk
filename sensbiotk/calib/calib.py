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
Calib for IMU sensors data
"""
import numpy as np
from sensbiotk.algorithms import basic as algo
from sensbiotk.calib import calib_acc as calib_acc
from sensbiotk.calib import calib_mag as calib_mag
from sensbiotk.calib import calib_gyr as calib_gyr

# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

SEP = ";"


def calib_imu_parameters(acc, mag, gyr):
    """ Compute IMU calibration parameters

    Parameters :
    ------------
    acc  : numpy array of float
                 accelerometers data motionless containing all the acquisition
                 on three axis
    mag : numpy array of float
                 magnetometers in motion containing all the acquisition
                 on three axis
    gyr : numpy array of float
                 gyrometers data motionless containing all the acquisition
                 on three axis

    Returns
    -------
     params : numpy array of float
             [ [off_accx off_accy off_accz], offset for accelerometers
             [sca_accx sca_accy sca_accz], scale for accelerometers
             [off_magx off_magy off_magz], offset for magnetometers
             [sca_magx sca_magy sca_magz], scale for magnetometers
             [off_gyrx off_gyry off_gyrz], offset for gyrometers
             [sca_gyrx sca_gyry sca_gyrz]] scale for gyrometers

    """

    # Accelerometers calibration parameters
    offset, scale = calib_acc.compute(acc)
    params_acc = np.append([offset], [scale[0, :]], axis=0)
    params_acc = np.append(params_acc, [scale[1, :]], axis=0)
    params_acc = np.append(params_acc, [scale[2, :]], axis=0)
    # Magnetometers calibration parameters
    offset, scale = calib_mag.compute(mag)
    params_mag = np.append([offset], [scale[0, :]], axis=0)
    params_mag = np.append(params_mag, [scale[1, :]], axis=0)
    params_mag = np.append(params_mag, [scale[2, :]], axis=0)
    # Gyrometers calibration parameters
    offset, scale = calib_gyr.compute(gyr)
    params_gyr = np.append([offset], [scale[0]], axis=0)
    params_gyr = np.append(params_gyr, [scale[1]], axis=0)
    params_gyr = np.append(params_gyr, [scale[2]], axis=0)

    return params_acc, params_mag, params_gyr


def save_param(filename, pcalib_acc, pcalib_mag, pcalib_gyr, comments=""):
    """ Save IMU calibration parameters

    Parameters :
    ------------
    filename : string
               filename to save
    pcalib_acc  : numpy array of float
             1x3 offset for accelerometers
              = [off_accx off_accy off_accz]
              3x3 matrix scale for accelerometers
    pcalib_mag  : numpy array of float
             1x3 offset for magnetometers
             = [off_magx off_magy off_magz]
             3x3 matrix scale for magnetometers
    pcalib_gyr  : numpy array of float
             1x3 offset for gyrometers
             = [off_gyrx off_gyry off_gyrz]
             3x3 matrix scale for gyrometers

    Returns
    -------
    None
    """

    fid = open(filename, 'w')
    # Write headers
    fid.write("# FOX calibration parameters (IMU file)\n")
    fid.write("# (c) INRIA 2011-2014\n")
    line = "# Comments: " + comments + "\n"

    lineformat = "%f"+SEP+"%f"+SEP+"%f\n"

    # Write accelerometers calibration parameters
    fid.write("# Offset for accelerometers\n")
    line = lineformat % (pcalib_acc[0][0], pcalib_acc[0][1], pcalib_acc[0][2])
    fid.write(line)
    # Write accelerometers calibration parameters
    fid.write("# Scale for accelerometers\n")
    line = lineformat % (pcalib_acc[1][0], pcalib_acc[1][1], pcalib_acc[1][2])
    fid.write(line)
    line = lineformat % (pcalib_acc[2][0], pcalib_acc[2][1], pcalib_acc[2][2])
    fid.write(line)
    line = lineformat % (pcalib_acc[3][0], pcalib_acc[3][1], pcalib_acc[3][2])
    fid.write(line)
    # Write magnetometers calibration parameters
    fid.write("# Offset for magnetometers\n")
    line = lineformat % (pcalib_mag[0][0], pcalib_mag[0][1], pcalib_mag[0][2])
    fid.write(line)
    fid.write("# Scale for magnetometers\n")
    line = lineformat % (pcalib_mag[1][0], pcalib_mag[1][1], pcalib_mag[1][2])
    fid.write(line)
    line = lineformat % (pcalib_mag[2][0], pcalib_mag[2][1], pcalib_mag[2][2])
    fid.write(line)
    line = lineformat % (pcalib_mag[3][0], pcalib_mag[3][1], pcalib_mag[3][2])
    fid.write(line)
    # Write gyrometers calibration parameters
    fid.write("# Offset for gyrometers\n")
    line = lineformat % (pcalib_gyr[0][0], pcalib_gyr[0][1], pcalib_gyr[0][2])
    fid.write(line)
    fid.write("# Scale for gyrometers\n")
    line = lineformat % (pcalib_gyr[1][0], pcalib_gyr[1][1], pcalib_gyr[1][2])
    fid.write(line)
    line = lineformat % (pcalib_gyr[2][0], pcalib_gyr[2][1], pcalib_gyr[2][2])
    fid.write(line)
    line = lineformat % (pcalib_gyr[3][0], pcalib_gyr[3][1], pcalib_gyr[3][2])
    fid.write(line)
    fid.close()

    return


def load_param(filename):
    """ Load IMU calibration parameters

    Parameters :
    ------------
    filename : string
               filename to load

    Returns
    -------
    params   : numpy array of float
             [ [off_accx off_accy off_accz], offset for accelerometers
             [sca_accx sca_accy sca_accz], scale for accelerometers
             [off_magx off_magy off_magz], offset for magnetometers
             [sca_magx sca_magy sca_magz], scale for magnetometers
             [off_gyrx off_gyry off_gyrz], offset for gyrometers
             [sca_gyrx sca_gyry sca_gyrz]] scale for gyrometers

    """

    params = np.loadtxt(filename, delimiter=SEP)

    pcalib_acc = params[0:4]
    pcalib_mag = params[4:8]
    pcalib_gyr = params[8:14]

    return pcalib_acc, pcalib_mag, pcalib_gyr


def print_param(params_acc, params_mag, params_gyr):
    """ Print IMU calibration parameters

    Parameters :
    ------------
    params : numpy array of float
           [ [off_accx off_accy off_accz], offset for accelerometers
             [sca_accx sca_accy sca_accz], scale for accelerometers
             [off_magx off_magy off_magz], offset for magnetometers
             [sca_magx sca_magy sca_magz], scale for magnetometers
             [off_gyrx off_gyry off_gyrz], offset for gyrometers
             [sca_gyrx sca_gyry sca_gyrz]] scale for gyrometers

    Returns
    -------
    None
    """

    print "Calibration Parameters"
    print "Accelerometers"
    print "Scale=", params_acc[0]
    print "Offset=\t", params_acc[1]
    print "\t", params_acc[2]
    print "\t", params_acc[3]
    print "Magnetometers"
    print "Scale=", params_mag[0]
    print "Offset=\t", params_mag[1]
    print "\t", params_mag[2]
    print "\t", params_mag[3]
    print "Gyrometers"
    print "Scale=", params_gyr[0]
    print "Offset=\t", params_gyr[1]
    print "\t", params_gyr[2]
    print "\t", params_gyr[3]

    return

FILETEST = "../../tests/data/imu08.csv"


def test1():
    """ Test1
    """
    from sensbiotk.io import iofox_deprec as fox
    from sensbiotk.io import viz

    print "Test Calibration"
    [time, acc, mag, gyr] = fox.load_foximu_csvfile(FILETEST)
    viz.plot_imu(0, "calib", time[:, 1], acc, mag, gyr)

    acc_motionless = acc[5500:7500]
    gyr_motionless = gyr[5500:7500]
    mag_motion = mag[8000:18000]

    scale, offset = calib_acc.compute_simple(acc_motionless)
    print "Acc"
    print "Scale=", scale
    print "Offset=", offset

    scale, offset = calib_mag.compute(mag_motion)
    print "Mag"
    print "Scale=", scale
    print "Offset=", offset

    scale, offset = calib_gyr.compute(gyr_motionless)
    print "Gyr"
    print "Scale=", scale
    print "Offset=", offset

    viz.plot_show()

    return


def test2():
    """ Test2
    """
    from sensbiotk.io import iofox_deprec as fox

    print "Test Calibration"
    data_file = FILETEST
    param_file = "param-imu08.csv"

    [_, acc, mag, gyr] = fox.load_foximu_csvfile(data_file)

    acc_motionless = acc[5500:7500]
    gyr_motionless = gyr[5500:7500]
    mag_motion = mag[8000:18000]

    p_acc, p_mag, p_gyr = calib_imu(acc_motionless,
                                    mag_motion,
                                    gyr_motionless)
    print "----- Parameters computed"
    print_param(p_acc, p_mag, p_gyr)
    save_param(param_file, p_acc, p_mag, p_gyr)
    p_acc = p_mag = p_gyr = []
    p_acc, p_mag, p_gyr = load_param(param_file)
    print "----- Parameters after load/save"
    print_param(p_acc, p_mag, p_gyr)

    return


def test3():
    """ Test3
    """
    from sensbiotk.io import iofox_deprec as fox
    import pylab as py

    print "Test Calibration"
    [_, acc, _, _] = fox.load_foximu_csvfile(FILETEST)

    norm_acc = algo.compute_norm(acc)

    py.plot(norm_acc)
    py.show()

    return

def compute(imuNumber, filepath=None, param=1):

    """ Performs IMU calibration parameters,
    saves them in a file at the same path than the .csv recording used,
    and returns them.

    Parameters :
    ------------
    params : integer
           imuNumber, the ID of the IMU to calibrate
            filepath
            string, the path to the .csv calibration file,
            if no path given, a GUI shows up
            param
            integer, 1 : only returns parameters
                     2 : only saves parameters
                     3 : saves and returns parameters

    Returns
    -------
    None
    """

    # MAIN PROCESS for loading a calibration recording,
    #computing the parameters and saving them in a file.
    from sensbiotk.io.uigetfile import uigetfile
    from sensbiotk.algorithms.basic import find_static_periods_3D
    from sensbiotk.io.iofox import load_foxcsvfile
    from os.path import split

    # Select and import IMU DATA
    if filepath is None:
        filepath = uigetfile(title= \
        'Select the IMU .csv file', filetypes=[('.csv file', '.csv')])
    [_, accx, accy, accz, mx, my, mz, gyrx, gyry, gyrz] = \
                load_foxcsvfile(filepath)
    freqs = 200

    # Detects the motionless periods (at least 2s and less than 4deg/s)
    start, end = \
    find_static_periods_3D(
    np.column_stack((gyrx, gyry, gyrz)), 10 * np.pi/180, 2*freqs)
    if len(start) == 0: # if no static periods found
        print "WARNING : NO STATIC PERIOD FOUND"

    # Computes the parameters
    acc_stat_x = []
    acc_stat_y = []
    acc_stat_z = []
    gyr_stat_x = []
    gyr_stat_y = []
    gyr_stat_z = []

    for i in range(0, len(start)):
        # Mean of each stationary state
        acc_stat_x.append(np.mean(accx[start[i]:end[i]+1]))

        acc_stat_y.append(np.mean(accy[start[i]:end[i]+1]))

        acc_stat_z.append(np.mean(accz[start[i]:end[i]+1]))

        # All the gyro values for each stationary state
        gyr_stat_x = np.concatenate((np.array(gyr_stat_x),
                                     gyrx[start[i]: end[i]]))
        gyr_stat_y = np.concatenate((np.array(gyr_stat_y),
                                     gyry[start[i]: end[i]]))
        gyr_stat_z = np.concatenate((np.array(gyr_stat_z),
                                     gyrz[start[i]: end[i]]))

    acc_stat = np.column_stack((acc_stat_x, acc_stat_y, acc_stat_z))
    mag = np.column_stack((mx, my, mz))
    gyr_stat = np.column_stack((gyr_stat_x, gyr_stat_y, gyr_stat_z))

    [params_acc, params_mag, params_gyr] = \
    calib_imu_parameters(acc_stat, mag, gyr_stat)

    if param == 1: #only returns parameters
        return params_acc, params_mag, params_gyr
    elif param == 2: #save parameters
        save_param(split(filepath)[0]+\
            "/CalibrationFileIMU"+str(imuNumber)+".txt",\
            params_acc, params_mag, params_gyr, comments="")
    elif param == 3: #save and return parameters
        save_param(split(filepath)[0]+\
            "/CalibrationFileIMU"+str(imuNumber)+".txt",\
            params_acc, params_mag, params_gyr, comments="")
        return params_acc, params_mag, params_gyr

