# -*- coding: utf-8 -*-# This file is a part of sensbiotk
# Contact : sensbiotk@inria.fr
# Copyright (C) 2015 INRIA
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
Basic script for converting multiple folders with Raw files
to a determined location, sorted both by experimentation number and by IMU.

For each IMU, extract all the files .RAW from the SD card and put it in a
folder with the following name : ImuNumber_Location

ex: (for IMU n°1 located on the right shank, the folder is : 1_RIGHT_SHANK

"""
import glob
import os
from sensbiotk.io import iofox
import shutil

# disabling pylint errors 'E1101' no-member, false positive from pylint
# pylint:disable=I0011,E1101

#the path to the data folders
RAW_DATA_LOCATION = \
    'C:/Users/bsijober/Desktop/data'

for root, dirs, files in os.walk(RAW_DATA_LOCATION):
    for name_dir in dirs:
        ImuNumber = name_dir[0]
        ImuLocation = name_dir[name_dir.find('_')+1:]
        fileNumber = 1
        os.chdir(RAW_DATA_LOCATION + '/' + name_dir)
        for onefile in sort(glob.glob("*.RAW")):
            fs = 200
            BASEFILE = str(fileNumber) + "_IMU" + ImuNumber + "_" + ImuLocation
            HOME = os.getenv("HOME")
            DATA = HOME + \
                "/ImuConvertedData/" + "IMU" + ImuNumber + "_" + ImuLocation
            DATAExpe = HOME + "/ImuConvertedData/" + str(fileNumber)
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
                [TIME, ACC, MAG, GYR] = \
                    iofox.load_foximu_csvfile(
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
                print "\n=>>> Successfully converted RAW file at Fs = " +\
                    str(fs) + "Hz to : " + HOME + "/ImuConvertedData/" + "\n"
                print str(file) + ' => ' + BASEFILE
                fileNumber = fileNumber + 1
            else:
                print "       Conversion failed"
