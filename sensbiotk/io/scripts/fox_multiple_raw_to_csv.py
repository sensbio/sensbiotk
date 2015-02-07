# -*- coding: utf-8 -*-
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
Basic script for converting multiple Raw file to a determined location,
sorted both by experimentation number and by IMU.
Arguments enables the user to enter the IMU number,
its location on the patient. and the sampling rate.

"""

import sys
import glob
import os
from sensbiotk.io import iofox
import shutil

LEN_ARG = len(sys.argv)

if (LEN_ARG < 3) or (LEN_ARG > 4):
    print "Usage: fox_MultipleRawToCSV.py imu_number imu_location fs(optional)"
    print "Example : fox_MultipleRawToCSV.py 4 RIGHT_SHANK 200"
    print "       Bad number of arguments"
else:
    imu_number = str(sys.argv[1])
    imu_location = str(sys.argv[2])
    if LEN_ARG == 3:
        fs = 200
    else:
        fs = str(sys.argv[3])

#    os.chdir(os.getcwd())
    os.chdir('j:')
    file_number = 1
    for onefile in sort(glob.glob("*.RAW")):
        fs = 200
        BASEFILE = str(file_number) +\
            "_IMU" + str(imu_number) + "_" + imu_location
        HOME = os.getenv("HOME")
        DATA = HOME +\
            "/ImuConvertedData/" + "IMU" + str(imu_number) + "_" + imu_location
        DATAExpe = HOME + "/ImuConvertedData/" + str(file_number)
        if not os.path.exists(DATA):
            os.makedirs(DATA)
        if not os.path.exists(DATAExpe):
            os.makedirs(DATAExpe)
        FILEACC = DATA + "/" + BASEFILE + "_acc.csv"
        FILEMAG = DATA + "/" + BASEFILE + "_mag.csv"
        FILEGYR = DATA + "/" + BASEFILE + "_gyr.csv"
        FILEPRESST = DATA + "/" + BASEFILE + "_presst.csv"
        FILEGPIO = DATA + "/" + BASEFILE + "_gpio.csv"
        ANS = iofox.convert_sensors_rawfile(
            str(onefile), FILEACC, FILEMAG, FILEGYR, FILEPRESST, FILEGPIO)
        if ANS == "OK":
            [TIME, ACC, MAG, GYR] = iofox.load_foximu_csvfile(
                FILEACC, FILEMAG, FILEGYR, 1 / float(fs), 1)
            iofox.save_foxsignals_csvfile(
                TIME, ACC, MAG, GYR, DATA + "/" + BASEFILE + '.csv')
            if os.path.isfile(DATA + "/" + BASEFILE + '_gpio.csv'):
                shutil.copy(DATA + "/" + BASEFILE + '_gpio.csv', DATAExpe)
            else:
                shutil.copy(DATA + "/" + BASEFILE + '.csv', DATAExpe)
            os.remove(FILEACC)
            os.remove(FILEMAG)
            os.remove(FILEGYR)
            print "\n=>>> Successfully converted RAW file at Fs = " + \
                str(fs) + "Hz to : " + HOME + "/ImuConvertedData/" + "\n"
            print str(file) + ' => ' + BASEFILE
            file_number = file_number + 1
        else:
            print "       Conversion failed"
