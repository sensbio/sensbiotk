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

""" fox_raw.py
convert/plot raw Fox filename [-cdbvtfpamgh] -i <raw_foxfilename or path>
                                      or --input=<raw_foxfilename or path>

for the output directory --dir<dirname> or -d<dirname>
for a new basename output --basename<basename> or -b<basename>
for time verification --verif or -v
for sample time  --time=<sample_time(sec)> or -t <sample_time(sec)>
for sample frequency --frequency=<frequency(Hz)> or -s <frequency(Hz)>
for plot IMU raw data --plot or -p
for plot accelero raw data --acc or -a
for plot magneto raw data --mag or -m
for plot gyro raw data --gyr or -g
for help use --help or -h
"""

import sys
import os
import getopt
import numpy as np
import matplotlib.pyplot as plt
from sensbiotk.io import iofox
from sensbiotk.io import viz


def getnamefiles(filename, newbasename, diroutput):
    """ getnamefiles
    """
    if len(filename) == 0:
        usage()
        sys.exit(2)
    # Compute output namefile
    basefile = os.path.basename(filename)
    basefile = os.path.splitext(basefile)[0]
    if newbasename != "":
        basename = basefile.split("_")[0]
#        print "BASE", basefile, basename
        if basename != basefile:
            basefile = basefile.replace(basename, newbasename)
        else:
            basefile = newbasename

    if os.path.isdir(diroutput):
        facc = diroutput + "/" + basefile + "_acc.csv"
        fmag = diroutput + "/" + basefile + "_mag.csv"
        fgyr = diroutput + "/" + basefile + "_gyr.csv"
    else:
        print "error: bad output directory"
        usage()
        sys.exit(2)

    return basefile, facc, fmag, fgyr


def plotsig(time, data, title, labely):
    """ Plot one signal """
    plt.figure()
    plt.title(title)
    plt.plot(time, data[:, 0:3])
    plt.ylabel(labely)
    plt.xlabel('time (s)')
    plt.legend(('x', 'y', 'z'))


def veriftime(label, ptime):
    """ Clock verification

    Parameters:
    ------------
    ptime: numpy array
    """
    plt.figure()
    plt.title(label)
    plt.grid()
    clock = np.diff(ptime)
    plt.plot(clock)

    print 'NB Points      =', len(ptime)
    print 'Duration    (s)=', ptime[-1] - ptime[0]
    print 'Steptime    (ms)=', (ptime[-1] - ptime[0]) / len(ptime)
    print 'Time to', ptime[0], 'From', ptime[-1]
    print 'Clock mean (ms)=', np.mean(clock)
    print 'Clock std  (ms)=', np.std(clock)
    print 'Clock max  (ms)=', np.max(clock)
    print 'Clock min  (ms)=', np.min(clock)
    return


def usage():
    """Usage command print
    """
    print "Usage"
    print __doc__


def main(argv):
    """ Main command
    """
    options = []
    filename = ""
    try:
        opts, _ = getopt.getopt(argv, "i:d:b:vt:f:pamgh",
                                ["input=", "dir=", "basename",
                                 "verif", "time=", "frequency=",
                                 "plot", "acc", "mag", "gyr", "help"])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    period = 0.005
    diroutput = "."
    newbasename = ""
    filenames = ""

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            fnames = arg
            if not os.path.isfile(fnames):
                if not os.path.isdir(fnames):
                    print "error: input file/dir does not exist"
                    usage()
                    sys.exit(2)
                else:
                    # directory input specified
                    filenames = os.listdir(fnames)
                    idx = 0
                    for onefile in filenames:
                        filenames[idx] = fnames + "/" + onefile
                        #filenames[idx] = fnames + "/" + filenames[idx]
                        idx = idx + 1
            else:
                # filename input specified
                filenames = [fnames]
        elif opt in ("-d", "--dir"):
            diroutput = arg
        elif opt in ("-b", "--basename"):
            newbasename = arg
        elif opt in ("-v", "--verif"):
            options.append("-v")
        elif opt in ("-t", "--time"):
            try:
                period = float(arg)
            except ValueError:
                usage()
                sys.exit(2)
            if period <= 0:
                usage()
                sys.exit(2)
        elif opt in ("-f", "--frequency"):
            try:
                period = float(arg)
            except ValueError:
                usage()
                sys.exit(2)
            if period <= 0:
                usage()
                sys.exit(2)
            else:
                period = 1 / period
        elif opt in ("-p", "--plot"):
            options.append("-p")
        elif opt in ("-a", "--acc"):
            options.append("-a")
        elif opt in ("-m", "--mag"):
            options.append("-m")
        elif opt in ("-g", "--gyr"):
            options.append("-g")

    if len(filenames) == 0:
        usage()
        sys.exit(2)

    for filename in filenames:
        print "Conversion:", filename
        # Get names file
        basefile, fileacc, filemag, filegyr =\
            getnamefiles(filename, newbasename, diroutput)
        # Read and convert file
        answer = iofox.convert_sensors_rawfile(filename,
                                               fileacc,
                                               filemag,
                                               filegyr)
        if answer != "OK":
            usage()
            sys.exit(2)
        # Load ascii files converted
        [myt, acc, mag, gyr] = \
            iofox.load_foximu_csvfile(fileacc, filemag, filegyr, period, 1)
        # Plot if necessary
        if "-p" in options:
            label = basefile + " IMU"
            viz.plot_imu(-1, label, myt, acc, mag, gyr)
        if "-a" in options:
            label = basefile + " Acc"
            plotsig(myt, acc, label, "ACC (m/s^2")
        if "-m" in options:
            label = basefile + " Mag"
            plotsig(myt, mag, label, "MAG (gauss)")
        if "-g" in options:
            label = basefile + " Gyr"
            plotsig(myt, gyr, label, "GYR (rad/s)")
        if "-v" in options:
            [myt, acc] = iofox.load_foxacc_csvfile(fileacc)
            label = basefile + " time verif."
            veriftime(label, myt[:, 0])

    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
