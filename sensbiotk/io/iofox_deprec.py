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
Loader for HikoB Fox Node format - deprecated data format
"""

import numpy as np
import struct

# pylint:disable= I0011, E1101, R0912, R0913, R0914, R0915
# E1101 no-member false positif

# Global dictionnaries
LSM303DLHC_ACC_SCALE = {'2g': 0x00, '4g': 0x10, '8g': 0x20, '16g': 0x30}
LSM303DLHC_MAG_SCALE = {'1_3gauss': 0x20, '1_9gauss': 0x40, '2_5gauss': 0x60,
                        '4_0gauss': 0x80, '4_7gauss': 0xA0, '5_6gauss': 0xC0,
                        '8_1gauss': 0xE0}
L3G4200D_SCALE = {'250dps': 0x00, '500dps': 0x10, '2000dps': 0x30}
SCALE = {'ref_g': 9.81, 'time': 1e-3,
         'acc': 2.0e-2, 'mag_xy': (1.0 / 670.0), 'mag_z': (1.0 / 600.0),
         'press': 1.0 / 4096.0 / 1000.0, 'temp': 1.0 / 480.0,
         'offset_temp': 22.5}
SEP = "\t"


def _get_acc_scale():
    """ get accelerometer scale

    Returns
    -------
    accelerometer : array of float
                  It contains [scale, min, max].
    """
    scale = SCALE['acc']
    return [scale, -2048 * scale, 2047 * scale]


def _get_magxy_scale():
    """g et magnetometer scale

    Returns
    -------
    magnetometer : array of float
                 It contains [scale, min, max]
    """
    scale = SCALE['mag_xy']
    return [scale, -2048 * scale, 2047 * scale]


def _get_gyr_scale():
    """ get gyrometer scale

    Returns
    -------
    gyrometer : array of float
              It contains [scale, min, max]
    """
    scale = SCALE['gyr']
    return [scale, -32768 * scale, 32767 * scale]


def _get_time(rawval):
    """ get time value from a binary format

    Parameters :
    ------------
    rawval: binary format
            time value

    Returns :
    ---------
    time : float
         value in second
    """
    val = struct.unpack("=HH", rawval)
    return SCALE['time'] * (val[1] * 65536 + val[0])


def _get_acc(rawval):
    """ get accelerometer values  from a binary format

    Parameters
    ----------
    rawval: binary format
            accelerometer values

    Returns
    -------
    accelerometer : numpy array of float
                  3 axis values  [ax,ay,az] in m/s^2
    """
    val = struct.unpack("=hhh", rawval)
    return SCALE['acc']*np.array([val[0], val[1], val[2]], dtype=float)


def _get_mag(rawval):
    """get magnetometer values  from a binary format

    Parameters :
    ------------
    rawval: binary format
          magnetometer values in gauss

    Returns :
    ---------
    magnetometer : numpy array of float
                 3 axis values [ax,ay,az]
    """
    val = struct.unpack("=hhh", rawval)
    return np.array([SCALE['mag_xy']*val[0], SCALE['mag_xy']*val[1],
                     SCALE['mag_z']*val[2]], dtype=float)


def _get_gyr(rawval):
    """ get gyrometer values  from a binary format

    Parameters
    ----------
    rawval: binary format
            gyrometer values

    Returns
    -------
    gyrometer : numpy array of float
              3 axis values [ax,ay,az] in rad/s
    """
    val = struct.unpack("=hhh", rawval)
    return SCALE['gyr'] * np.array([val[0], val[1], val[2]], dtype=float)


def _get_press(rawval):
    """ get pression value from a binary format

    Parameters
    ----------
    rawval: binary format
          pression value

    Returns
    -------
    pression : float
             value in bar
    """
    val = struct.unpack("=BBB", rawval)
    return SCALE['press'] * (val[0] + (val[1] << 8) + (val[2] << 16))


def _get_temp(rawval):
    """ get temperature value from a binary format

    Parameters
    ----------
    rawval: binary format
            temperature value

    Returns
    -------
    temperature : float
                value in degree
    """
    val = struct.unpack("=h", rawval)
    return SCALE['offset_temp'] + SCALE['temp'] * val[0]


def _set_time_scale(val):
    """ set time scale value

    Parameters
    ----------
    val: float
         time scale in second
    """
    SCALE['time'] = val

    return


def _set_acc_scale(val):
    """ set accelerometer scale value

    Parameters
    ----------
    val: float
        accelerometer scale value in m/s^2
    """
    if val == LSM303DLHC_ACC_SCALE['2g']:
        SCALE['acc'] = 1e-3 * SCALE['ref_g']
    elif val == LSM303DLHC_ACC_SCALE['4g']:
        SCALE['acc'] = 2e-3 * SCALE['ref_g']
    elif val == LSM303DLHC_ACC_SCALE['8g']:
        SCALE['acc'] = 4e-3 * SCALE['ref_g']
    elif val == LSM303DLHC_ACC_SCALE['16g']:
        SCALE['acc'] = 12e-3 * SCALE['ref_g']
    return


def _set_mag_scale(val):
    """ set magnetometer scale value

    Parameters
    ----------
    val: magnetometer scale value
    """
    if val == LSM303DLHC_MAG_SCALE['1_3gauss']:
        SCALE['mag_xy'] = 1.0 / 1100.0
        SCALE['mag_z'] = 1.0 / 980.0
    elif val == LSM303DLHC_MAG_SCALE['1_9gauss']:
        SCALE['mag_xy'] = 1.0 / 850.0
        SCALE['mag_z'] = 1.0 / 760.0
    elif val == LSM303DLHC_MAG_SCALE['2_5gauss']:
        SCALE['mag_xy'] = 1.0 / 670.0
        SCALE['mag_z'] = 1.0 / 600.0
    elif val == LSM303DLHC_MAG_SCALE['4_0gauss']:
        SCALE['mag_xy'] = 1.0 / 450.0
        SCALE['mag_z'] = 1.0 / 400.0
    elif val == LSM303DLHC_MAG_SCALE['4_7gauss']:
        SCALE['mag_xy'] = 1.0 / 400.0
        SCALE['mag_z'] = 1.0 / 355.0
    elif val == LSM303DLHC_MAG_SCALE['5_6gauss']:
        SCALE['mag_xy'] = 1.0 / 330.0
        SCALE['mag_z'] = 1.0 / 295.0
    elif val == LSM303DLHC_MAG_SCALE['8_1gauss']:
        SCALE['mag_xy'] = 1.0 / 230.0
        SCALE['mag_z'] = 1.0 / 205.0

    return


def _set_gyr_scale(val):
    """ set gyrometer scale value

    Parameters
    ----------
    val: float
         gyrometer scale value in rad/sec
    """
    if val == L3G4200D_SCALE['250dps']:
        SCALE['gyr'] = 8.75e-3 * np.pi / 180.0
    elif val == L3G4200D_SCALE['500dps']:
        SCALE['gyr'] = 1.75e-2 * np.pi / 180.0
    elif val == L3G4200D_SCALE['2000dps']:
        SCALE['gyr'] = 7e-2 * np.pi / 180.0

    return


def _write_imu_header(fid, binfilename):
    """ write the IMU header file

    Parameters
    ----------
    fid : file object opened
          file to be writted
    binfilename : str
          binary filename readed
    """
    fid.write("# FOX Logger (IMU file)\r\n")
    fid.write("# (c) INRIA 2013\r\n")
    fid.write("#")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# id\tt\tdt\tax\tay\taz\tmx\tmy\tmz\tgx\tgy\tgz\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tAcceleration: m.s^-2\r\n")
    fid.write("#\tMagnetic field: gauss\r\n")
    fid.write("#\tRotation speed: rad.s^-1\r\n")
    fid.write("#\r\n")

    return


def _write_imu_data(fid, data):
    """ write a IMU data line

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys definded must be :
    'id':int, 't':float, 'acc':[float,float,float],
    'mag':[float,float,float],'gyr':[float,float,float]
    """

    lineformat = "%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n"
    delta = data['t'] - _write_presst_data.lastt
    line = lineformat % (data['id'], data['t'], delta,
                         data['acc'][0], data['acc'][1], data['acc'][2],
                         data['mag'][0], data['mag'][1], data['mag'][2],
                         data['gyr'][0], data['gyr'][1], data['gyr'][2])
    fid.write(line)
    _write_imu_data.lastt = data['t']

    return

_write_imu_data.lastt = 0


def _write_presst_header(fid, binfilename):
    """ Write the pression and temperature header file.

    Parameters
    ----------
    fid : file object opened
        file to be writted
    """
    fid.write("# FOX Logger (pression and temperature file)\r\n")
    fid.write("# (c) INRIA 2013\r\n")
    fid.write("#")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# id\tt\tdt\tpression\ttemperature\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tPression: bar\r\n")
    fid.write("#\tTemperature: degree (C)\r\n")
    fid.write("#\r\n")

    return


def _write_presst_data(fid, data):
    """ Write a pression and temperature data line.

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys defined must be :
    'id':int, 't':float, 'pression':float, 'temperature':float
    """
    lineformat = "%s\t%f\t%f\t%f\t%f\r\n"
    delta = data['t'] - _write_presst_data.lastt
    line = lineformat % (data['id'], data['t'],
                         delta, data['press'], data['temp'])
    fid.write(line)
    _write_presst_data.lastt = data['t']

    return

_write_presst_data.lastt = 0


def convert_fox_rawfile(binfilename, imufilename, presstfilename):
    """ Convert a raw bin HikoB Fox file into an ascii csv files.

    Parameters
    ----------
    binfilename : str
                Name of the raw file to load and convert.
    imufilename : str
                Name of the csv imu file
    presstfilename : str
                   Name of the presst file

    Returns
    -------
    status : str
             "OK" or "ERROR"
    """

    with open(binfilename, "rb") as in_fox:
        out_imu = open(imufilename, 'w')
        out_presst = open(presstfilename, 'w')
        # Read Header Name
        buf = in_fox.read(5)
        if len(buf) != 5:
            print "Error while reading file"
            return "ERROR"
        else:
            name = struct.unpack("=ccccc", buf)
            if "".join(name) != "HiKoB":
                print "Error while reading file"
                return "ERROR"
        # Read Scale
        buf = in_fox.read(4)
        if len(buf) != 4:
            print "Error while reading file"
            return "ERROR"
        else:
            val = struct.unpack("=BBBB", buf)
            version = val[0]
            _set_acc_scale(val[1])
            _set_mag_scale(val[2])
            _set_gyr_scale(val[3])
            if version < 2:
                _set_time_scale(1e-3)
                imu_size = 22
                presst_size = 9
            else:
                _set_time_scale(1.0 / 32768.0)
                imu_size = 22
                presst_size = 10
            # Read data packets
            cont = True
            imu = {'id': 0, 't': 0.0, 'acc': [0.0, 0.0, 0.0],
                   'mag': [0.0, 0.0, 0.0], 'gyr': [0.0, 0.0, 0.0]}
            presst = {'id': 0, 't': 0.0, 'press': 0.0, 'temp': 0.0}
            _write_imu_header(out_imu, binfilename)
            _write_presst_header(out_presst, binfilename)

            while cont is True:
                buf = in_fox.read(4)
                if len(buf) != 4:
                    cont = False
                else:
                    idb = struct.unpack("=HH", buf)
                    sensid = idb[1] * 65536 + idb[0]
                    if version == 0:
                        typ = sensid >> 30
                    else:
                        typ = sensid >> 28
                    if typ == 0:
                        buf = in_fox.read(imu_size)
                        if len(buf) != imu_size:
                            cont = False
                        else:
                            if version == 0:
                                imu['id'] = sensid & (0x3FFFFFFF)
                            else:
                                imu['id'] = sensid & (0x0FFFFFFF)
                            imu['t'] = _get_time(buf[0:4])
                            imu['acc'] = _get_acc(buf[4:10])
                            imu['mag'] = _get_mag(buf[10:16])
                            imu['gyr'] = _get_gyr(buf[16:22])
                            _write_imu_data(out_imu, imu)
                    elif typ == 3:
                        buf = in_fox.read(presst_size)
                        if len(buf) != presst_size:
                            cont = False
                        else:
                            if version == 0:
                                presst['id'] = sensid & (0x3FFFFFFF)
                            else:
                                presst['id'] = sensid & (0x0FFFFFFF)
                            presst['t'] = _get_time(buf[0:4])
                            presst['press'] = _get_press(buf[4:7])
                            presst['temp'] = _get_temp(buf[8:10])
                            _write_presst_data(out_presst, presst)

                        if len(buf) != 10:
                            cont = False
        in_fox.close()
        out_imu.close()
        out_presst.close()

    return "OK"


def info_fox_rawfile(binfilename):
    """ Extract info. HikoB Fox Node from a raw bin file.

    Parameters
    ----------
    filename : str
             Name of the bin file to load.
    """

    ret = convert_fox_rawfile(binfilename, "imuf.txt", "press.txt")

    return ret


def load_foximu_csvfile(filename):
    """ Load IMU HikoB Fox Node from a CSV file.

    Parameters
    ----------
    filename: str
            Name of the CSV file to load.

    Returns
    -------
    tabA numpy array which contains id
    """
    imu = np.loadtxt(filename)

    # Split data
    time = imu[:, 0:3]
    acc = imu[:, 3:6]
    mag = imu[:, 6:9]
    gyr = imu[:, 9:12]

    return [time, acc, mag, gyr]


def load_foxpresst_csvfile(filename):
    """ Load Pression/Temperature HikoB Fox Node from a CSV file.

    Parameters
    ----------
    filename: str
            Name of the CSV file to load.

    Returns
    -------
    time : np.array
          The matrix contains time [id,time,dt],  pression (bar)
          and temperature (degree). id is an int and time,dt,bar
          and degree are float values.
    """
    presst = np.loadtxt(filename)

    # Split data
    time = presst[:, 0:3]
    press = presst[:, 3]
    temp = presst[:, 4]

    return [time, press, temp]


def save_foximu_csvfile(accfilename, time, acc, mag, gyr, separator=SEP):
    """ save a ascii csv file accelerometers IMU HikoB Fox file

    Parameters
    ----------
    accfilename : str
                Name of the csv imu file
    time : numpy array
         [t, dt]
    acc : numpy array
         [ax ay az]
    mag : numpy array
         [mx my mz]
    gyr : numpy array
         [gx gy gz]

    Returns
    -------
    status : str
             "OK" or "ERROR"
    """

    out_acc = open(accfilename, 'w')
    _write_imu_header(out_acc, "sensbiotk output")
    lineformat = "%d" + separator + "%f" + separator + "%f" + separator + \
                 "%f" + separator + "%f" + separator + "%f" + separator + \
                 "%f" + separator + "%f" + separator + "%f" + separator + \
                 "%f" + separator + "%f" + separator + "%f" + separator + \
                 + "\r\n"
    for index in range(0, len(time)):
        line = lineformat % (time[index, 0], time[index, 1], time[index, 2],
                             acc[index, 0], acc[index, 1], acc[index, 2],
                             mag[index, 0], mag[index, 1], mag[index, 2],
                             gyr[index, 0], gyr[index, 1], gyr[index, 2])
        out_acc.write(line)

    out_acc.close()

    return "OK"
