# -*- coding: utf-8; -*-
# This file is a part of sensbiotk
# Contact : sensbiotk@inria.fr
# Copyright (C) 2015  INRIA
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
Loader/Saver for attitude and heading reference system (ahrs)
"""

import numpy as np

# pylint:disable= I0011, E1101
# E1101 no-member false positif


def _write_header(fid):
    """ write the AHRS header file

    Parameters
    ----------
    fid : file object opened
          file to be writted
    """
    fid.write("# AHRS Logger (IMU file)\r\n")
    fid.write("# (c) INRIA 2011-2014\r\n")
    fid.write("#\r\n# File format:\r\n")
    fid.write("# id" + "\t" + "t" + "\t" + "dt" + "\t" + "qw" +
              "\t" + "qx" + "\t" + "qy" + "\t" + "qz" + "\t" +
              "roll" + "\t" + "pitch" + "\t" + "yaw \r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tQuaternion: none\r\n")
    fid.write("#\tAngle: radians\r\n")
    fid.write("#\r\n")

    return


def _write_data(fid, data):
    """ write a AHRS data line

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data : dictionnary
        The keys definded must be :
        't':float, 'acc':[float,float,float], 'mag':[float,float,float],
        gyr':[float,float,float]

    Returns
    -------
    None

    """

    lineformat = "%f" + "\t" + "%f" + "\t" + "%f" + "\t"\
        + "%f" + "\t" + "%f" + "\t" + "%f" + "\t" + "%f" + "\t"\
        + "%f\r\n"

    line = lineformat % (data['t'], data['quat'][0],
                         data['quat'][1], data['quat'][2], data['quat'][3],
                         data['euler'][0], data['euler'][1], data['euler'][2]
                         )
    fid.write(line)

    return


def save_ahrs_csvfile(filename, time, quat, ang_euler):
    """ save a ascii csv ahrs file with the format line :\n
    t qw qx qy qz roll pitch yaw

    The colon separation is a tab

    Parameters
    ----------
    time : numpy.array
         in second
    quat : numpy array
         [qw, qx qy qz]
    ang_euler : numpy array
         angles in radians
         [roll pitch yaw]
    filename : str
        The ouput .csv file name

    Returns
    -------
    status : str
             'OK' / 'ERROR'

    Examples
    --------
     >>> timu = [0, 1]
     >>> quat = [[1,0,0,0], [1,0,0,0]]
     >>> euler = [[0,0,0], [0,0,0]]
     >>> save_ahrs_csvfile("data/ahrs.csv", timu, quat, euler)
    """

    out = open(filename, 'w')
    _write_header(out)

    data = {'t': 0.0, 'quat': [0.0, 0.0, 0.0, 0.0], 'euler': [0.0, 0.0, 0.0]}

    for index in range(0, len(time)):
        data['t'] = time[index]
        data['quat'] = quat[index, :]
        data['euler'] = ang_euler[index, :]
        _write_data(out, data)

    out.close()

    return 'OK'


def load_ahrs_csvfile(filename):
    """ Load Ahrs data from a CSV file version with the format line :

    t   qw    qx    qy    qz    roll    pitch    yaw

    The colon separation is a tab

    Parameters
    -----------
    filename : str
            Name of the CSV file containing ahrs  data

    Returns
    -------
    time : numpy.array
           time in sec
    quat : numpy.array
           [qw, qx, qy, qz]
    euler : numpy.array
           angles in radians
           [roll, pitch, yaw]

     Examples
     --------
     >>> timu, quat, euler = load_ahrs_csvfile("data/output_ahrs.csv")
     >>> print quat
    """

    data = np.loadtxt(filename, delimiter='\t')

    time = data[:, 0]
    quat = np.column_stack((data[:, 1], data[:, 2], data[:, 3], data[:, 4]))
    euler = np.column_stack((data[:, 5], data[:, 6], data[:, 7]))

    return time, quat, euler
