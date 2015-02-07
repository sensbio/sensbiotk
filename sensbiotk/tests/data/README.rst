====================
SensbioTK data tests
====================

Directory which contains data to test SensbioTK software.
The filenames are constructed using a rootname and some extensions
in convention:
* rootname.raw : binary raw file created by the sensors FOX HikoB
* rootname_acc.csv : csv file which contains accelerometers data
* rootname_mag.csv : csv file which contains magnetometers data
* rootname_gyr.csv : csv file which contains gyrometers data
* rootname_gpio.csv : csv file which contains gpio data (produced 
by a Fox HikoB with a daughter board)
* rootname_presst.csv : csv file which contains pressure and temperature data
 
Files
========

imutest_deprec* : IMU sample data used in test_iofox_deprec.py
imutest* : IMU sample data used in test_iofox.py
doortest_big* : IMU sample data (big size) used in test_iofox.py. The sensor
is located on a door.
gpiotest* : GPIO sample data (big size) used in test_iofox.py

SUB-DIRECTORY
==============
* calib_accelerometer : data used in test_calib.py
