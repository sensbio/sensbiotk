basics
======
Building scripts for IMU data exploitation. 

Script                              |       function 
----------------------------------------------------------------------------
`fox_raw.py`                        |
`fox_calib.py`                      | IMU sensors calibration
`fox_angle.py`                      | 
`fox_multiple_raw_to_csv.py`        | Converting multiple Raw file to a 
                                    |  determined location
`fox_multiple_raw_folder_to_CSV.py` | Converting multiple folders with Raw files

You can use the environment variable PATH to call these scripts from anyware.

Scripts are self-documented, and usually have sub-commands which are
also self-documented. Use e.g:

fox_raw.py --help

### ``fox_raw.py``

```
Usage
 fox_raw.py
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
```
