import serial
import re
import threading
import time
import math
import logging
from serial.tools import list_ports

class FoxSink():
    """ Class to manage sink node data reading """

    def __init__(self):
        """Class Initialization"""
        # Flag/Control of data acquisition thread
        self.run = False
        # sink node id
        self.id = 0
        # sink node time
        self.time = 0
        # sample time count imu node
        self.count = 0
        # pyserial serial link
        self.ser = None
        # linux name of the serial link
        self.linename = ''
        # sensors data
        self.sensor = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.line = ' '
        self.a_scale = 4e-3 * 9.81
        self.m_scale_xy = 1.0 / 670.0
        self.m_scale_z  = 1.0 / 600.0
        self.g_scale = 1.75e-2 * math.pi / 180.0
        # Thread identifier
        self.t_task = 0
        self.t_task_exception = ''
        # User callback called
        self.callback = None
        return

    def connect_serial(self):
        """Search the right USB serial line
        if line found self.ser and self.line  are set and
        the connection is established

        Returns :
        ---------
        found : boolean
                line found (True) or not (False)
        """

        timeout = 2 #sec

        for port in list_ports.comports():
            try:
                if 'COM5' in port[0]:
                    baudrate = 500000
                    self.ser = serial.Serial(port[0], baudrate = baudrate, timeout = timeout)
                    # Send a init/reset cmd to found the fox on the serial line
                    if self.fox_init() is True:
                        self.ser.close()
                        self.ser = serial.Serial(port[0], baudrate = baudrate, timeout = 0)
                        self.line = port[0]
                        return True # line found
            except Exception as e:
                pass

        return False # not found


    def __fox_write_command(self, command, response):
        """Write a Fox command on serial. Check response.

        Returns :
        ---------
        cmd_ok : boolean, True if command succeed. else False.
        """

        try:
            self.ser.write(command)
            data = self.ser.read(64)
            if len(data) != 0 and response in data:
                return True # ok
        except Exception as e:
            pass
        return False


    def fox_init(self):
        """Init the Fox

        Returns :
        ---------
        cmd_ok : boolean
                 The init of the fox pedometer is launched (True)
                 or failed (False)
        """

        return True
        #return self.__fox_write_command("FI\n", "FOX_BANET:init_ok")

    
    def fox_run(self):
        """Run the data measure on Fox

        Returns :
        ---------
        cmd_ok : boolean
                 The run on fox pedometer is launched (True)
                 or failed (False)
        """

        return True
        #return self.__fox_write_command("FR\n", "FOX_BANET:run_ok")


    def fox_close(self):
        """Reset the Fox

        Returns :
        ---------
        cmd_ok : boolean
                 The close fox pedometer is ok (True) or failed (False)
        """

        #cmd_ok = self.__fox_write_command("FI\n", "FOX_BANET:init_ok")

        # **close** serial line
        try:
            self.ser.close()
        except Exception as e:
            pass

        self.run = False
        return True
        #return cmd_ok

    
    def analyse(self):
        """Set criteria values by analysing sink node message"""

	# data read from the serial line has the following format:
        # node_id:time count ax ay az mx my my gz gx gy gz
	# C1CA:30 9 0 0 0 0 0 0 0 0 0 
        
	ptn = re.compile('(?P<node_id>[0-9A-F]+):(?P<sink_time>[0-9]+)\t(?P<sens_count>[0-9]+)\t(?P<ax>[\-0-9]+)\t(?P<ay>[\-0-9]+)\t(?P<az>[\-0-9]+)\t(?P<mx>[\-0-9]+)\t(?P<my>[\-0-9]+)\t(?P<mz>[\-0-9]+)\t(?P<gx>[\-0-9]+)\t(?P<gy>[\-0-9]+)\t(?P<gz>[\-0-9]+)')

        result = ptn.match(self.line)
        if result:
            self.nodeid = result.group('node_id')
            self.time = int(result.group('sink_time'))
            self.count  = int(result.group('sens_count'))
            self.sensor[0] = self.a_scale * int(result.group('ax'))
            self.sensor[1] = self.a_scale * int(result.group('ay'))
            self.sensor[2] = self.a_scale * int(result.group('az')) 
            self.sensor[3] = self.m_scale_xy * int(result.group('mx'))
            self.sensor[4] = self.m_scale_xy * int(result.group('my'))
            self.sensor[5] = self.m_scale_z * int(result.group('mz')) 
            self.sensor[6] = self.g_scale * int(result.group('gx'))
            self.sensor[7] = self.g_scale * int(result.group('gy'))
            self.sensor[8] = self.g_scale * int(result.group('gz'))
        else:
                logging.debug('ERROR: Bad format sink node message')
                logging.debug('line="%s"' % (self.line.replace('\r', '\\r').replace('\n', '\\n')))

                
    def set_callback(self, funcname = None):
        """Set function callback to be called during reading"""
        self.callback = funcname


    def read_serial(self):
        """Loop reading the rs232/usb line sink node
           put the message in self.line and update sensor data
           values
        """

        data = ''
        self.t_task_exception = ''

        try:
            while self.run:
                time.sleep(0.001)
                data += self.ser.read(1024)
                if '\r\n' in data:
                    end_ix = data.index('\r\n')+2
                    self.line = data[:end_ix]
                    data = data[end_ix:]
                    self.analyse()

                    if not self.callback is None:
                        self.callback()

        except Exception as e:
            self.t_task_exception = str(e)
            logging.error(str(e))

        self.run = False
        logging.error('>>> thread terminated')
        return


    def start_read(self):
        """ Launch a thread for read_usb """

        if not self.run:
            self.t_task = threading.Thread(None, self.read_serial, None)
            self.run = True
            self.t_task.start()
            logging.debug('OK: thread started')
        else:
            logging.debug('ERROR: Thread sink node starting failed')


    def stop_read(self):
        """ Stop the reading thread """

        if self.run:
            self.run = False
            self.t_task.join(5)
            logging.debug('OK: thread stopped')
        else:
            logging.debug('ERROR: Thread sink node stopping failed')


def test3():
    """ Read directly the sink node without GUI
        launching a thread
        stop with ctl-C
    """

    def read_callback():
        """ acq. function callback"""
        print '>', sinknode.sensor

    sinknode = FoxSink()

    print 'Enter acquisition loop (type ^C to stop).'

    connected = False
    while True:
        try:
            if not connected:
                if sinknode.connect_serial():
                    connected = True
                    print "Line connected at %s" % (sinknode.line)
                    sinknode.fox_run()
                    sinknode.set_callback(read_callback)
                    sinknode.start_read()
                    print 'Read started.'
                else:
                    time.sleep(1)

            if connected:
                if sinknode.run:
                    time.sleep(1)
                else:
                    sinknode.stop_read()
                    connected = False
                    print 'Line disconnected (%s).\nRead stopped.' % (sinknode.t_task_exception)

        except KeyboardInterrupt:
            print "\nStopped."
            break
        except Exception as e:
            logging.error('exception reached:' + str(e))

    sinknode.stop_read()

##
if __name__ == '__main__':
    test3()
