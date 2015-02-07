import logging
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import fox_dongle


def test_acq_callback(obj):
    """ Fake function to test callback"""
#    print "Nb of sample", len(obj.data)


def update(index, fdongle, aaxes, maxes, gaxes):
#    print index, len(fdongle.data)
    if fdongle.data != [] :
        aaxes[1].set_data(fdongle.data[:,1], fdongle.data[:,2])
        aaxes[2].set_data(fdongle.data[:,1], fdongle.data[:,3])
        aaxes[3].set_data(fdongle.data[:,1], fdongle.data[:,4])
        maxes[1].set_data(fdongle.data[:,1], fdongle.data[:,5])
        maxes[2].set_data(fdongle.data[:,1], fdongle.data[:,6])
        maxes[3].set_data(fdongle.data[:,1], fdongle.data[:,7])
        gaxes[1].set_data(fdongle.data[:,1], fdongle.data[:,8])
        gaxes[2].set_data(fdongle.data[:,1], fdongle.data[:,9])
        gaxes[3].set_data(fdongle.data[:,1], fdongle.data[:,10])
        
    aaxes[0].relim()
    aaxes[0].autoscale_view(True, True, True) 
    maxes[0].relim()
    maxes[0].autoscale_view(True, True, True) 
    gaxes[0].relim()
    gaxes[0].autoscale_view(True, True, True)
    return


def fplot(fdongle): 
    # set up animation
    fig = plt.figure()
    plt.title("Fox live")
    aaxes = [None, None, None, None]
    axa = fig.add_subplot(311)
    aaxes[0] = axa
    aaxes[1], = axa.plot([], [])
    aaxes[2], = axa.plot([], [])
    aaxes[3], = axa.plot([], [])
    plt.ylabel('ACC (m/s^2)')
    maxes = [None, None, None, None]
    axm = fig.add_subplot(312)
    maxes[0] = axm
    maxes[1], = axm.plot([], [])
    maxes[2], = axm.plot([], [])
    maxes[3], = axm.plot([], [])
    plt.ylabel('MAG (gauss)')
    gaxes = [None, None, None, None]
    axg = fig.add_subplot(313)
    gaxes[0] = axg
    gaxes[1], = axg.plot([], [])
    gaxes[2], = axg.plot([], [])
    gaxes[3], = axg.plot([], [])
    plt.ylabel('Gyr (rad/s)')

    anim = animation.FuncAnimation(fig, update,
                                   fargs=(fdongle, aaxes, maxes, gaxes ),
                                   interval=100)
    plt.show()
    close(fdongle)
    exit(0)
    return


def close(fdongle):
    from sensbiotk.io import iofox as fox
    print "\nStopped and Record in tmp_imu.csv."
    if fdongle.data != [] :
        resp = fox.save_foxsignals_csvfile(fdongle.data[:, 1], 
                                           fdongle.data[:, 2:5],
                                           fdongle.data[:, 5:8],
                                           fdongle.data[:, 8:11],
                                           "tmp_imu.csv")
    fdongle.close_dongle()
    return

    
def live():
    """ Example of use of the Fox Sink dongle
    """
    from sensbiotk.io import iofox as fox

    # instanciate dongle
    foxdongle = fox_dongle.FoxDongle()

    print 'Enter acquisition loop (type ^C to stop and save tmp_imu.csv).'

    init = False
    plotinit = False

    while True:
        try:
            # handle dongle initialization
            if not init and foxdongle.init_dongle(test_acq_callback):
                init = True
                print 'Device is connected to %s.' % (foxdongle.line())
            if not plotinit:
                fplot(foxdongle)
                plotinit = True

            time.sleep(5)
        except KeyboardInterrupt:
            print "\nStopped and Record in tmp_imu.csv."
            if foxdongle.data != [] :
                resp = fox.save_foxsignals_csvfile(foxdongle.data[:, 1], 
                                                   foxdongle.data[:, 2:5],\
                                                   foxdongle.data[:, 5:8],\
                                                   foxdongle.data[:, 8:11],
                                                   "tmp_imu.csv")
            break
        except Exception as e:
            logging.error('exception reached:' + str(e))
           

    # must close to kill read thread (fox_sink)
    foxdongle.close_dongle()
    print 'Done'
    return

if __name__ == '__main__':
    live()
