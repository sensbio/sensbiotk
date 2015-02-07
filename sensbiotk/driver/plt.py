from sensbiotk.io import iofox as fox
import pylab as py


#[time, acc, mag, gyr] = fox.load_foxcsvfile("tmp_imu.csv")

[time, ax, ay, az, mx, my, mz, gx, gy, gz] = \
    fox.load_foxcsvfile("tmp_imu.csv")

py.figure()
py.title("Fox logging")
ax1 = py.subplot(311)
py.plot(time, ax)
py.plot(time, ay)
py.plot(time, az) 
py.ylabel('ACC (m/s^2)')
py.subplot(312)
py.plot(time, mx)
py.plot(time, my)
py.plot(time, mz)
py.ylabel('MAG (gauss)')
py.subplot(313)
py.plot(time, gx)
py.plot(time, gy)
py.plot(time, gz)
py.ylabel('GYR (rad/s)')
py.xlabel('time (s)')
py.show()
