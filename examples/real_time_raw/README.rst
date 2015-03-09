14/01/14

# Setup

* sink node (banet_sink.elf) connected to the PC with USB and HikoB programmator
* imu node (banet_imu.elf) for logging IMU values and send to sink node each 40 ms

# Launch record
> python fox_console.py

Enter acquisition loop (type ^C to stop and save tmp_imu.csv).
Device is connected to /dev/ttyUSB1.
Nb of sample 11
Nb of sample 2
Nb of sample 3
Nb of sample 4
Nb of sample 5
Nb of sample 6
Nb of sample 7
Nb of sample 8
Nb of sample 9
Nb of sample 10
Nb of sample 11
Nb of sample 12
Nb of sample 13
Nb of sample 14
Nb of sample 15
Nb of sample 16
^C
Stopped and Record in tmp_imu.csv.
Done
ERROR:root:Attempting to use a port that is not open
ERROR:root:>>> thread terminated

When the fox_dongle.py if connection is ok, the line 'Nb of sample' is printed.
When you want to stop and save the file tmp_imu.csv, type ^C

# Plot recording

When the fox_dongle.py if connection is ok, the line 'Nb of sample' is printed.
When you want to stop and save the file tmp_imu.csv, type ^C
Then you can plot data recorded
> python plt.py
