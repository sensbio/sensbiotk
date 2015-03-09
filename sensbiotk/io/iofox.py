# -*- coding: utf-8; -*-
# This file is a part of sensbiotk
# Contact: sensbiotk@inria.fr
# Copyright (C) 2014  INRIA 
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
Loader for HikoB Fox Node format
"""

import numpy as np
import scipy.interpolate as spi
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
SEP = ";"
TIME_OVERFLOW = 8192.0


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
    """ g et magnetometer scale

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


def _get_gpio(rawval):
    """ get gpio value from a binary format

    Parameters
    ----------
    rawval: binary format
             gpio value

    Returns
    -------
    gpio : int
           GPIO value
    """
    val = struct.unpack("=B", rawval)

    return val[0]


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


def _write_header(fid, binfilename):
    """ write the IMU header file

    Parameters
    ----------
    fid : file object opened
          file to be writted
    binfilename : str
          binary filename readed
    """
    fid.write("# FOX Logger (IMU file)\r\n")
    fid.write("# (c) INRIA 2011-2014\r\n")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# id" + "\t" + "t" + "\t" + "dt" + "\t" + "ax"
              + "\t" + "ay" + "\t" + "az" + "\t" + "mx" + "\t"
              + "my" + "\t" + "mz" + "\t" + "gx" + "\t" + "gy"
              + "\t" + "gz\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tAcceleration: m.s^-2\r\n")
    fid.write("#\tMagneto: gauss\r\n")
    fid.write("#\tGyrometer: rad/s\r\n")
    fid.write("#\r\n")

    _write_data.lastt = 0
    _write_data.lastid = 1

    return


def _write_acc_header(fid, binfilename):
    """ write the accelerometers IMU header file

    Parameters
    ----------
    fid : file object opened
          file to be writted
    binfilename : str
          binary filename readed
    """
    fid.write("# FOX Logger (IMU file)\r\n")
    fid.write("# (c) INRIA 2011-2014\r\n")
    fid.write("#\r\n")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# t"+SEP+"dt"+SEP+"ax"+SEP+"ay"+SEP+"az\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tAcceleration: m.s^-2\r\n")
    fid.write("#\r\n")

    _write_acc_data.lastt = 0

    return


def _write_mag_header(fid, binfilename):
    """ write the magnetometers IMU header file

    Parameters
    ----------
    fid : file object opened
          file to be writted
    binfilename : str
          binary filename readed
    """
    fid.write("# FOX Logger (IMU file)\r\n")
    fid.write("# (c) INRIA 2011-2014\r\n")
    fid.write("#\r\n")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# t"+SEP+"dt"+SEP+"mx"+SEP+"my"+SEP+"mz\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tMagnetic field: gauss\r\n")
    fid.write("#\r\n")

    _write_mag_data.lastt = 0

    return


def _write_gyr_header(fid, binfilename):
    """ write the gyrometers IMU header file

    Parameters
    ----------
    fid : file object opened
          file to be writted
    binfilename : str
          binary filename readed
    """
    fid.write("# FOX Logger (IMU file)\r\n")
    fid.write("# (c) INRIA 2011-2014\r\n")
    fid.write("#\r\n")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# t"+SEP+"dt"+SEP+"gx"+SEP+"gy"+SEP+"gz\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tRotation speed: rad.s^-1\r\n")
    fid.write("#\r\n")

    _write_gyr_data.lastt = 0

    return


def _write_presst_header(fid, binfilename):
    """ Write the pression and temperature header file.

    Parameters
    ----------
    fid : file object opened
        file to be writted
    """
    fid.write("# FOX Logger (pression and temperature file)\r\n")
    fid.write("# (c) INRIA 2011-2014\r\n")
    fid.write("#\r\n")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# t"+SEP+"dt"+SEP+"tpression"+SEP+"temperature\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tPression: bar\r\n")
    fid.write("#\tTemperature: degree (C)\r\n")
    fid.write("#\r\n")

    _write_presst_data.lastt = 0

    return


def _write_gpio_header(fid, binfilename):
    """ Write the GPIO header file.

    Parameters
    ----------
    fid : file object opened
        file to be writted
    """
    fid.write("# FOX Logger (GPIO file)\r\n")
    fid.write("# (c) INRIA 2011-2014\r\n")
    fid.write("#\r\n")
    line = "# File created from file "+binfilename+"\r\n"
    fid.write(line)
    fid.write("#\r\n# File format:\r\n")
    fid.write("# t" + SEP + "dt" + SEP + "gpio0" + SEP + "gpio1"
              + SEP + "gpio2" + SEP + "gpio3" + SEP + "gpio4\r\n")
    fid.write("#\r\n# Units:\r\n")
    fid.write("#\tTime: s\r\n")
    fid.write("#\tGPIO: 0/1\r\n")
    fid.write("#\r\n")

    _write_gpio_data.lastt = 0

    return


def _write_acc_data(fid, data):
    """ write a accelerometers IMU data line

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys definded must be :
         't':float, 'acc':[float,float,float],
    """

    lineformat = "%f"+SEP+"%f"+SEP+"%f"+SEP+"%f"+SEP+"%f\r\n"
    delta = data['t'] - _write_acc_data.lastt

    line = lineformat % (data['t'], delta,
                         data['acc'][0], data['acc'][1], data['acc'][2])

    fid.write(line)
    _write_acc_data.lastt = data['t']

    return


def _write_data(fid, data):
    """ write a IMU data line

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys definded must be :
         't':float, 'acc':[float,float,float], 'mag':[float,float,float],
         'gyr':[float,float,float]
    """

    lineformat = "%i" + "\t" + "%f" + "\t" + "%f" + "\t" + "%f" + "\t"\
        + "%f" + "\t" + "%f" + "\t" + "%f" + "\t" + "%f" + "\t"\
        + "%f" + "\t" + "%f" + "\t" + "%f" + "\t" + "%f\r\n"
    delta = data['t'] - _write_data.lastt
   # id=1
    line = lineformat % (_write_data.lastid, data['t'], delta,
                         data['acc'][0], data['acc'][1], data['acc'][2],
                         data['mag'][0], data['mag'][1], data['mag'][2],
                         data['gyr'][0], data['gyr'][1], data['gyr'][2],
                         )

    fid.write(line)
    _write_data.lastt = data['t']
    _write_data.lastid = _write_data.lastid+1

    return


def _write_mag_data(fid, data):
    """ write a magnetometers IMU data line

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys definded must be :
         't':float, 'mag':[float,float,float],
    """

    lineformat = "%f"+SEP+"%f"+SEP+"%f"+SEP+"%f"+SEP+"%f\n"
    delta = data['t']-_write_mag_data.lastt
    line = lineformat % (data['t'], delta,
                         data['mag'][0], data['mag'][1], data['mag'][2])

    fid.write(line)
    _write_mag_data.lastt = data['t']

    return


def _write_gyr_data(fid, data):
    """ write a gyrometers IMU data line

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys definded must be :
         't':float, 'gyr':[float,float,float],
    """

    lineformat = "%f" + SEP + "%f" + SEP + "%f" + SEP + "%f" + SEP + "%f\r\n"
    delta = data['t']-_write_gyr_data.lastt
    line = lineformat % (data['t'], delta,
                         data['gyr'][0], data['gyr'][1], data['gyr'][2])

    fid.write(line)
    _write_gyr_data.lastt = data['t']
    return

_write_gyr_data.lastt = 0


def _write_presst_data(fid, data):
    """ Write a pression and temperature data line.

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys defined must be :
        't':float, 'pression':float, 'temperature':float
    """
    lineformat = "%f"+SEP+"%f"+SEP+"%f"+SEP+"%f\r\n"
    delta = data['t'] - _write_presst_data.lastt
    line = lineformat % (data['t'], delta, data['press'], data['temp'])
    fid.write(line)
    _write_presst_data.lastt = data['t']

    return


def _write_gpio_data(fid, data):
    """ Write GPIOs

    Parameters
    ----------
    fid : file object opened
        file to be writted
    data: dictionnary
        The keys defined must be :
        't':float, 'gpio0:int, 'gpio1':float, 'gpio2:int,
                   'gpio3':float, 'gpio4':float
    """
    lineformat = "%f" + SEP + "%f" + SEP + "%u" + SEP + "%u" + SEP\
        + "%u" + SEP + "%u" + SEP + "%u\r\n"
    delta = data['t'] - _write_gpio_data.lastt
    line = lineformat % (data['t'], delta, data['gpio0'], data['gpio1'],
                         data['gpio2'], data['gpio3'], data['gpio4'])
    fid.write(line)
    _write_gpio_data.lastt = data['t']

    return


def convert_sensors_rawfile(binfilename, accfilename="output_acc.csv",
                            magfilename="output_mag.csv",
                            gyrfilename="output_gyr.csv",
                            presstfilename="output_presst.csv",
                            gpiofilename="output_gpio.csv"):

    """ Convert a raw bin HikoB Fox sensors file into an ascii csv files.

    Parameters
    ----------
    binfilename : str
                Name of the raw file to load and convert.
    accfilename : str
                Name of the csv accelerometers imu file
    magfilename : str
                Name of the csv magnetometers imu file
    gyrfilename : str
                Name of the csv gyrometers imu file
    presstfilename : str
                Name of the csv pressure & temperature sensors file
    gpiofilename : str
                Name of the csv gpio file
    Returns
    -------
    status : str
             'OK' / 'ERROR'
    """

    with open(binfilename, "rb") as in_fox:

        # Read Header Name
        buf = in_fox.read(5)
        if len(buf) != 5:
            print "Error while reading file"
            return 'ERROR'
        else:
            name = struct.unpack("=ccccc", buf)
            if "".join(name) != "HiKoB":
                print "Error while reading file"
                return 'ERROR'
        # Read Scale
        buf = in_fox.read(4)
        if len(buf) != 4:
            print "Error while reading file"
            return 'ERROR'
        else:
            val = struct.unpack("=BBBB", buf)
            version = val[0]
            if version < 4:
                print "File version: ", version, " is to old"
                return 'ERROR'
            _set_acc_scale(val[1])
            _set_mag_scale(val[2])
            _set_gyr_scale(val[3])

            _set_time_scale(1.0 / 32768.0)
            offset_time = 0.0
            prec_time = 0.0

            sensor_size = 6
            presst_size = 6
            gpio_size = 1

            # Read the AHRS_ENABLED byte and drop it
            in_fox.read(1)
            # Sensors data initialization
            acc = {'t': 0.0, 'acc': [0.0, 0.0, 0.0]}
            mag = {'t': 0.0, 'mag': [0.0, 0.0, 0.0]}
            gyr = {'t': 0.0, 'gyr': [0.0, 0.0, 0.0]}
            presst = {'t': 0.0, 'press': 0.0, 'temp': 0.0}
            gpio = {'t': 0.0, 'gpio': [0.0, 0.0, 0.0, 0.0, 0.0]}

            # Flags to write output header file one time
            header_acc = True
            header_mag = True
            header_gyr = True
            header_presst = True
            header_gpio = True
            # Flags to control the loop
            cont = True
            err = False
            # Read data packets
            while cont is True:
                buf = in_fox.read(4)
                if len(buf) != 4:
                    cont = False
                else:
                    # Read Time and Id sensor
                    idb = struct.unpack("=HH", buf)
                    sensid = idb[1]*65536+idb[0]
                    sensid = sensid & 0x0FFFFFFF
                    current_time = (SCALE['time'] * sensid) + offset_time
                    if prec_time > (current_time + 8000.0):
                        offset_time = offset_time + TIME_OVERFLOW
                        current_time = current_time + TIME_OVERFLOW
                    prec_time = current_time

                    typ = (idb[1] & 0xF000) >> 12
                    # ACC packet
                    if typ == 0x5:
                        if header_acc:
                            out_acc = open(accfilename, 'w')
                            _write_acc_header(out_acc, binfilename)
                            header_acc = False
                        buf = in_fox.read(sensor_size)
                        if len(buf) != sensor_size:
                            cont = False
                        else:
                            acc['t'] = current_time
                            acc['acc'] = _get_acc(buf)
                            _write_acc_data(out_acc, acc)
                    # MAG packet
                    elif typ == 0x6:
                        if header_mag:
                            out_mag = open(magfilename, 'w')
                            _write_mag_header(out_mag, binfilename)
                            header_mag = False
                        buf = in_fox.read(sensor_size)
                        if len(buf) != sensor_size:
                            cont = False
                        else:
                            mag['t'] = current_time
                            mag['mag'] = _get_mag(buf)
                            _write_mag_data(out_mag, mag)
                    # GYR packet
                    elif typ == 0x7:
                        if header_gyr:
                            out_gyr = open(gyrfilename, 'w')
                            _write_gyr_header(out_gyr, binfilename)
                            header_gyr = False
                        buf = in_fox.read(sensor_size)
                        if len(buf) != sensor_size:
                            cont = False
                        else:
                            gyr['t'] = current_time
                            gyr['gyr'] = _get_gyr(buf)
                            _write_gyr_data(out_gyr, gyr)
                    # Pressure sensor packet
                    elif typ == 0x3:
                        if header_presst:
                            out_presst = open(presstfilename, 'w')
                            _write_presst_header(out_presst, binfilename)
                            header_presst = False
                        buf = in_fox.read(presst_size)
                        if len(buf) != presst_size:
                            cont = False
                        else:
                            presst['t'] = current_time
                            presst['press'] = _get_press(buf[0:3])
                            presst['temp'] = _get_temp(buf[4:6])
                            _write_presst_data(out_presst, presst)
                    # GPIOs packet
                    elif typ == 0x8:
                        if header_gpio:
                            out_gpio = open(gpiofilename, 'w')
                            _write_gpio_header(out_gpio, binfilename)
                            header_gpio = False
                        buf = in_fox.read(gpio_size)
                        if len(buf) != gpio_size:
                            cont = False
                        else:
                            gpio['t'] = current_time
                            gpio['gpio0'] = (_get_gpio(buf[0])) & 1
                            gpio['gpio1'] = (_get_gpio(buf[0]) >> 1) & 1
                            gpio['gpio2'] = (_get_gpio(buf[0]) >> 2) & 1
                            gpio['gpio3'] = (_get_gpio(buf[0]) >> 3) & 1
                            gpio['gpio4'] = (_get_gpio(buf[0]) >> 4) & 1
                            _write_gpio_data(out_gpio, gpio)

            in_fox.close()
            if header_acc is False:
                out_acc.close()
            if header_mag is False:
                out_mag.close()
            if header_gyr is False:
                out_gyr.close()
            if header_presst is False:
                out_presst.close()
            if header_gpio is False:
                out_gpio.close()
            if err is True:
                return 'ERROR'

    return 'OK'


def load_foxacc_csvfile(filename):
    """ Load Acceleration IMU HikoB Fox Node from a CSV file.

    Parameters
    ----------
    filename : str
            Name of the CSV file to load.

    Returns
    -------
    two numpy array which contains [t,dt] and [accx,accy,accz]

    """
    imu_acc = np.loadtxt(filename, delimiter=SEP)

    # Split data
    time = imu_acc[:, 0:2]
    acc = imu_acc[:, 2:5]

    return [time, acc]


def load_foxmag_csvfile(filename):
    """ Load Magnetometers IMU HikoB Fox Node from a CSV file.

    Parameters
    ----------
    filename : str
            Name of the CSV file to load.

    Returns
    -------
    two numpy array which contains [t,dt] and [magx,magy,magz]

    """
    imu_mag = np.loadtxt(filename, delimiter=SEP)

    # Split data
    time = imu_mag[:, 0:2]
    mag = imu_mag[:, 2:5]

    return [time, mag]


def load_foxgyr_csvfile(filename):
    """ Load Gyrometers IMU HikoB Fox Node from a CSV file.

    Parameters
    ----------
    filename : str
            Name of the CSV file to load.

    Returns
    -------
    two numpy array which contains [t,dt] and [gyrx,gyry,gyrz]

    """
    imu_gyr = np.loadtxt(filename, delimiter=SEP)

    # Split data
    time = imu_gyr[:, 0:2]
    gyr = imu_gyr[:, 2:5]

    return [time, gyr]


def load_foxpresst_csvfile(filename):
    """ Load Pression/Temperature HikoB Fox Node from a CSV file.

    Parameters
    ----------
    filename: str
            Name of the CSV file to load.

    Returns
    -------
    time : np.array
          The matrix contains time [time,dt],  pression (bar)
          and temperature (degree). id is an int and time,dt,bar
          and degree are float values.
    """
    presst = np.loadtxt(filename, delimiter=SEP)

    # Split data
    time = presst[:, 0:2]
    press = presst[:, 2]
    temp = presst[:, 3]

    return [time, press, temp]


def load_foxgpio_csvfile(filename):
    """ Load Gpio HikoB Fox Node from a CSV file.

    Parameters
    ----------
    filename : str
            Name of the CSV file to load.

    Returns
    -------
   [time, gpio] : np.array
          The matrix contains time [time,dt],
          gpio1 (0/1), gpio2 (0/1)
          gpio3 (0/1), gpio4 (0/1), gpio5 (0/1)
    """
    gpios = np.loadtxt(filename, delimiter=SEP)

    # Split data
    time = gpios[:, 0:2]
    gpio = gpios[:, 2:7]

    return [time, gpio]


def _spline_resample(sig_x, sig_y, sig_xnew, deg_spline):
    """ Resample signal with B-Spline

    Parameters
    ----------
    sig_x: np.array
            signal sample time
    sig_y: np.array
            signal value
    sig_xnew: np.array
             signal sample time for the resampling
    deg_spline: int
            the order of the spline fit.  1 <= k <= 5
    Returns
    -------
    for numpy array which contains the signal resampled
    sig_xnew
    """
    sig = spi.splrep(sig_x, sig_y, k=deg_spline)
    sig_ynew = spi.splev(sig_xnew, sig)

    return sig_ynew


def load_foximu_csvfile(filename_acc, filename_mag, filename_gyr,
                        dtime, deg_s=1):
    """ Load IMU HikoB Fox Node from a CSV file version 2

    Parameters
    ----------
    filename_acc : str
            Name of the CSV files to load accelerometers
    filename_mag : str
            Name of the CSV files to load magnetometers
    filename_gyr : str
            Name of the CSV files to load gyrometers
    dtime: float
            sampling period in seconds
    deg_s : int
           the order of the spline fit used for signal resampling.  1 <= k <= 5

    Returns
    -------
    [t_interp, acc_interp, mag_interp, gyr_interp] : numpy.array

    for numpy array which contains t_interp, acc_interp = [accx,accy,accz],
    mag_interp = [magx,magy,magz], gyr_interp = [gyrx,gyry,gyrz]
    """

    # load IMU signals with their own sample time
    [t_acc, acc] = load_foxacc_csvfile(filename_acc)
    [t_mag, mag] = load_foxmag_csvfile(filename_mag)
    [t_gyr, gyr] = load_foxgyr_csvfile(filename_gyr)
    # search the common timeline
    tmin = np.max([t_acc[0, 0], t_mag[0, 0], t_gyr[0, 0]])
    tmax = np.min([t_acc[-1, 0], t_mag[-1, 0], t_gyr[-1, 0]])
    t_interp = np.arange(tmin, tmax, dtime)
    if t_interp[-1] < tmax:
        t_interp = np.append(t_interp, [tmax], axis=0)
    # Trunk signals to keep the common timeline
    index = 0
    while t_acc[index, 0] < tmin:
        t_acc[index, 0] = np.delete(t_acc[index, 0], index, axis=0)
        acc[index, 0] = np.delete(acc[index, 0], index, axis=0)
        index = index+1
    index = 0
    while t_mag[index, 0] < tmin:
        t_mag[index, 0] = np.delete(t_mag[index, 0], index, axis=0)
        mag[index, 0] = np.delete(mag[index, 0], index, axis=0)
        index = index+1
    index = 0
    while t_gyr[index, 0] < tmin:
        t_gyr[index, 0] = np.delete(t_gyr[index, 0], index, axis=0)
        gyr[index, 0] = np.delete(gyr[index, 0], index, axis=0)
        index = index+1
    index = -1
    while t_acc[index, 0] > tmax:
        t_acc[index, 0] = np.delete(t_acc[index, 0], index, axis=0)
        acc[index, 0] = np.delete(acc[index, 0], index, axis=0)
        index = index-1
    index = -1
    while t_mag[index, 0] > tmax:
        t_mag[index, 0] = np.delete(t_mag[index, 0], index, axis=0)
        mag[index, 0] = np.delete(mag[index, 0], index, axis=0)
        index = index-1
    index = -1
    while t_gyr[index, 0] > tmax:
        t_gyr[index, 0] = np.delete(t_gyr[index, 0], index, axis=0)
        gyr[index, 0] = np.delete(gyr[index, 0], index, axis=0)
        index = index-1
    # initialize signals array
    s_size = len(t_interp)
    acc_interp = np.zeros((s_size, 3))
    mag_interp = np.zeros((s_size, 3))
    gyr_interp = np.zeros((s_size, 3))
    # resample signals
    acc_interp[:, 0] = _spline_resample(t_acc[:, 0], acc[:, 0],
                                        t_interp, deg_s)
    acc_interp[:, 1] = _spline_resample(t_acc[:, 0], acc[:, 1],
                                        t_interp, deg_s)
    acc_interp[:, 2] = _spline_resample(t_acc[:, 0], acc[:, 2],
                                        t_interp, deg_s)
    mag_interp[:, 0] = _spline_resample(t_mag[:, 0], mag[:, 0],
                                        t_interp, deg_s)
    mag_interp[:, 1] = _spline_resample(t_mag[:, 0], mag[:, 1],
                                        t_interp, deg_s)
    mag_interp[:, 2] = _spline_resample(t_mag[:, 0], mag[:, 2],
                                        t_interp, deg_s)
    gyr_interp[:, 0] = _spline_resample(t_gyr[:, 0], gyr[:, 0],
                                        t_interp, deg_s)
    gyr_interp[:, 1] = _spline_resample(t_gyr[:, 0], gyr[:, 1],
                                        t_interp, deg_s)
    gyr_interp[:, 2] = _spline_resample(t_gyr[:, 0], gyr[:, 2],
                                        t_interp, deg_s)

    # py.plot(t_interp, gyr_interp[:, 0], 'bo-')
    # py.plot(t_gyr[:, 0], gyr[:, 0], 'ro-')
    # py.figure()
    # py.plot(t_interp, acc_interp[:, 0], 'bo-')
    #  py.plot(t_acc[:, 0], acc[:, 0], 'ro-')
    # py.show()

    return [t_interp, acc_interp, mag_interp, gyr_interp]


def load_foxcsvfile(filename):
    """ Load IMU HikoB Fox Node data from a CSV file version 2\n
    id    t    dt    ax    ay    az    mx    my    mz    gx    gy    gz\n
    columns are separated by a tab

    Parameters
    ----------
    filename : str
    Name of the CSV file containing inertial data

    Return
    -------
    time : numpy.array
    accx : numpy.array
    accy : numpy.array
    accz : numpy.array
    magx : numpy.array
    magy : numpy.array
    magz : numpy.array
    gyrx : numpy.array
    gyry : numpy.array
    gyrz : numpy.array
    """

    data = np.loadtxt(filename, delimiter='\t')

    time = data[:, 1]
    accx = data[:, 3]
    accy = data[:, 4]
    accz = data[:, 5]
    magx = data[:, 6]
    magy = data[:, 7]
    magz = data[:, 8]
    gyrx = data[:, 9]
    gyry = data[:, 10]
    gyrz = data[:, 11]

    return [time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz]


def save_foxsignals_csvfile(time, acc, mag, gyr, filename):
    """ save a ascii csv file with the following structure using
         time, acc, mag and gyr numpy arrays:
    # id    t    dt    ax    ay    az    mx    my    mz    gx    gy    gz

    Parameters
    ----------
    time signal : numpy array [t, dt]
    acc : numpy array
         [ax ay az]
    mag : numpy array
         [mx my mz]
    gyr : numpy array
         [gx gy gz]
    gpio : numpy array
         [gpio0 gpio1 gpio2 gpio3 gpio4]
    filename : str
        The ouput .csv file name

    Returns
    -------
    status : str
             'OK' or 'ERROR'
    """
    out = open(filename[:-3] + 'csv', 'w')
    _write_header(out, "sensbiotk output")

    data = {'t': 0.0, 'acc': [0.0, 0.0, 0.0], 'mag': [0.0, 0.0, 0.0],
            'gyr': [0.0, 0.0, 0.0]}

    for index in range(0, len(time)):
        data['t'] = time[index]
        data['acc'] = acc[index, :]
        data['mag'] = mag[index, :]
        data['gyr'] = gyr[index, :]
        _write_data(out, data)

    out.close()

    return 'OK'


def save_foxacc_csvfile(accfilename, time, acc):
    """ save a ascii csv file accelerometers IMU HikoB Fox file

    Parameters
    ----------
    accfilename : str
                Name of the csv imu file
    time : numpy array
         [t, dt]
    acc : numpy array
         [ax ay az]

    Returns
    -------
    status : str
             'OK' or 'ERROR'
    """

    out_acc = open(accfilename, 'w')

    _write_acc_header(out_acc, "sensbiotk output")

    data = {'t': 0.0, 'acc': [0.0, 0.0, 0.0]}

    for index in range(0, len(time)):
        data['t'] = time[index, 0]
        data['acc'] = acc[index, :]
        _write_acc_data(out_acc, data)

    out_acc.close()

    return 'OK'


def save_foxmag_csvfile(magfilename, time, mag):
    """ save a ascii csv file magnetometers IMU HikoB Fox file

    Parameters
    ----------
    accfilename : str
                Name of the csv imu file
    time : numpy array
         [t, dt]
    mag : numpy array
         [mx my mz]

    Returns
    -------
    status : str
             'OK' or 'ERROR'
    """

    out_mag = open(magfilename, 'w')

    _write_mag_header(out_mag, "sensbiotk output")

    data = {'t': 0.0, 'mag': [0.0, 0.0, 0.0]}

    for index in range(0, len(time)):
        data['t'] = time[index, 0]
        data['mag'] = mag[index, :]
        _write_mag_data(out_mag, data)

    out_mag.close()

    return 'OK'


def save_foxgyr_csvfile(gyrfilename, time, gyr):
    """ save a ascii csv file gyrometers IMU HikoB Fox file

    Parameters
    ----------
    accfilename : str
                Name of the csv imu file
    time : numpy array
         [t, dt]
    gyr : numpy array
         [mx my mz]

    Returns
    -------
    status : str
             'OK' / 'ERROR'
    """

    out_gyr = open(gyrfilename, 'w')

    _write_gyr_header(out_gyr, "sensbiotk output")

    data = {'t': 0.0, 'gyr': [0.0, 0.0, 0.0]}

    for index in range(0, len(time)):
        data['t'] = time[index, 0]
        data['gyr'] = gyr[index, :]
        _write_gyr_data(out_gyr, data)

    out_gyr.close()

    return 'OK'
