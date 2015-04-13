#!/usr/bin/python
# -*- coding: utf-8 -*-
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

# pylint:disable= I0011, E1101, R0912, R0913, R0914, R0915
# E1101 no-member false positif

"""
Fox IMU sensors calibration
"""
import sys
import argparse
import sensbiotk.calib.calib as calib

DEF_CALIBFILE = "calib_imu.txt"


def param(datacalibfile, calibfile, comments=""):
    """ Load or compute calibration parameters
    """
    [params_acc, params_mag, params_gyr] = \
        calib.compute(imuNumber=5, filepath=datacalibfile, param=3)
    calib.save_param(calibfile,
                     params_acc, params_mag, params_gyr, comments)

    return [params_acc, params_mag, params_gyr]


def launch():
    """ Launch the process taking into account arguments
    """
    # create parser
    parser = argparse.ArgumentParser(description="Fox IMU Calibration")
    # add arguments
    parser.add_argument('datafile', metavar='fox_imu_data.csv',
                        type=str, nargs=1,
                        help="Input motion dedicated to calibration")
    parser.add_argument('-o', '--output', type=str,
                        help="Fox IMU calibration parameters")
    args = parser.parse_args()
    # Arguments verification
    if len(args.datafile) != 1:
        parser.print_help()
        sys.exit()
    inputfile = args.datafile[0]
    if args.output is None:
        args.output = DEF_CALIBFILE
    outputfile = args.output

    # Launch the process
    print "CALIB", inputfile, outputfile
    [_, _, _] = param(inputfile, outputfile)


if __name__ == '__main__':
    launch()
