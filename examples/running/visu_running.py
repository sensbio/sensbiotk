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
Example for plotting data coming from
a FOX Inertial Measurement Unit (IMU)
27/11/12 - RPG
"""
from sensbiotk.io import iofox_deprec as fox
from sensbiotk.io import viz


def visu_running():
    """  plotting of a running
    """
    # Fichier ascii de donnees FOX
    filename = "./data/imu11.csv"

    # Read IMU data
    [time, acc_imu, mag_imu, gyr_imu] = fox.load_foximu_csvfile(filename)
    # Split data
    time_imu = time[:, 1]

    viz.plot_imu(1, "FOX IMU sensors", time_imu, acc_imu, mag_imu, gyr_imu)
    viz.plot_show()
    return

if __name__ == '__main__':
    visu_running()
