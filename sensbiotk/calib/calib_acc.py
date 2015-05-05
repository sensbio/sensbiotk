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
Calib algo for accelerometers sensors data
"""
import numpy as np
from sensbiotk.algorithms import basic as algo

# pylint:disable= I0011, E1101, R0913, R0914, R0915
# E1101 no-member false positif
# R0913 too-many-arguments
# R0914 too-many-locals
# R0915 too-many-statements

SEP = ";"


def scale_fit(data, constant):
    """ Compute scale from a constant signal to fit with a constant

    Parameters :
    ------------
    data : numpy array of float
           [sx sy sz] data sensor containing all the acquisition
           on three axis
    constant : float
           value to be fitted ajusting scale

    Returns
    -------
    offset :numpy array of float (dim=3)
     scale parameters
    """

    scale = [0, 0, 0]
    print "Warning:: scale_fit not implemented"
    print data, constant

    return scale


def scale_fit_norm(data, constant):
    """ Compute scale from a constant signal to fit with a constant

    Parameters :
    ------------
    data : numpy array of float
           [sx sy sz] data sensor containing all the acquisition
           on three axis
    constant : float
           value to be fitted ajusting scale

    Returns
    -------
    offset :float (dim=1)
     scale parameters

     Notes
     -----
     To allow a good fitting, The motion must cover all axis
     rotation without high acceleration.
    """
    scale = constant / np.mean(data)

    return scale


def compute(data):
    """
    Computes the Scale factor Matrix and the bias vector of a
    MEMS accelerometer.
    The procedure exploits the fact that, in static conditions, the
    modulus of the accelerometer output vector matches that of the
    gravity acceleration. The calibration model incorporates the bias
    and scale factor for each axis and the cross-axis symmetrical
    actors. The parameters are computed through Gauss-Newton nonlinear
    optimization.

    The mathematical model used is
    A = M(V - B)
    where M (scale) and B (bias) are scale factor matrix and
    bias vector respectively.

    M = [ Mxx Mxy Mxz; Myx Myy Myz; Mzx Mzy Mzz ];
         where  Mxy = Myx; Myz = Mzy; Mxz = Mzx;
    B = [ Bx; By; Bz ];

    The diagonal elements of M represent the scale factors along the
    three axes, whereas the other elements of M are called cross-axis
    factors. These terms allow describing both the axes misalignment
    and the crosstalk effect between different channels caused
    by the sensor electronics. In an ideal world, M = 1; B = 0

    --------------------------------------------------------------
    scale, biais = calibaccel( data )
    --------------------------------------------------------------

    Parameters
    ----------
    data : np.array
    (x,3) columns ax, ay and az acceleration values obtained from
    the accelerometer represented in m.s-2
     x rows represent averaged data from x different static positions

    Returns
    -------
    scale : np.array
        the scale factor matrix

    biais : np.array
        the bias vector (in m.s-2)
    """

    # Remove aberrant values (with norm too far from 9.81 => not a static position) 
    data_corr =[]
    for i in range(0, len(data)):  
        if (np.linalg.norm(data[i,:]) < 10.3) & (np.linalg.norm(data[i,:]) > 9.3):
            data_corr.append(data[i,:])
    data = np.array(data_corr)
    
    # For the solution converges, the recording has to be done in each axis direction. If it is not the case
    # we add the missing direction to the data
    missing_axis = np.array([0.0,0.0,0.0])   
    for i in range (0,3):    
        if np.max(np.abs(data[:,i]))<9:
            missing_axis[i] = 9.81            
            data = np.append(data, missing_axis).reshape(-1,3)
            data = np.append(data, -missing_axis).reshape(-1,3)
            missing_axis = np.array([0.0,0.0,0.0])    
            
    # Configurable variables
    # Damping Gain - Start with 1
    _lambda = 1
    # Damping paremeter - has to be less than 1.
    # Changing this will affect rate of convergence;
    # Recommend to use k1 between 0.01 - 0.05
    k_l = 0.01
    # Convergence criterion threshold
    tol = 1e-09
    # Better to leave this No. big.
    r_old = 10000000
    # No. Of iterations. If your solutions don't converge
    # then try increasing this. Typically it should converge
    # within 20 iterations
    itr = 50

    # Initial Guess values of M and B.  Change this only if you need to
    mxx0 = 5
    mxy0 = 0.5
    mxz0 = 0.5
    myy0 = 5
    myz0 = 0.5
    mzz0 = 5

    b_x0 = 0.5
    b_y0 = 0.5
    b_z0 = 0.5

    #   Algorithm
    vold = 0

    v_d = data
    (r_d, c_d) = v_d.shape

    if r_d < 9:
        print 'WARNING !!! Need atleast 9 Measurements for a correct calibration procedure! \n'

    if c_d != 3:
        print 'Not enough columns in the data'
        return 0, 0

    v_x = v_d[:, 0]
    v_y = v_d[:, 1]
    v_z = v_d[:, 2]

    m_d = len(v_d)
    r_j = np.zeros((m_d, 1))
    jac = np.zeros((m_d, 9))
    v_k = np.array([[mxx0, mxy0, mxz0, myy0, myz0, mzz0, b_x0, b_y0, b_z0]])

    # iterate
    for k in range(0, itr + 1):
        # Calculate the Jacobian at every iteration
        for i in range(0, len(v_x)):
            r_j[i] = errorf(v_x[i], v_y[i], v_z[i],
                            mxx0, mxy0, mxz0,
                            myy0, myz0, mzz0,
                            b_x0, b_y0, b_z0)
            jac[i, 0] = jac1(v_x[i], v_y[i], v_z[i],
                             mxx0, mxy0, mxz0,
                             b_x0, b_y0, b_z0)
            jac[i, 1] = jac2(v_x[i], v_y[i], v_z[i],
                             mxx0, mxy0, mxz0, myy0, myz0,
                             b_x0, b_y0, b_z0)
            jac[i, 2] = jac3(v_x[i], v_y[i], v_z[i],
                             mxx0, mxy0, mxz0, myz0, mzz0,
                             b_x0, b_y0, b_z0)
            jac[i, 3] = jac4(v_x[i], v_y[i], v_z[i],
                             mxy0, myy0, myz0,
                             b_x0, b_y0, b_z0)
            jac[i, 4] = jac5(v_x[i], v_y[i], v_z[i],
                             mxy0, mxz0, myy0, myz0, mzz0,
                             b_x0, b_y0, b_z0)
            jac[i, 5] = jac6(v_x[i], v_y[i], v_z[i],
                             mxz0, myz0, mzz0,
                             b_x0, b_y0, b_z0)
            jac[i, 6] = jac7(v_x[i], v_y[i], v_z[i],
                             mxx0, mxy0, mxz0,
                             myy0, myz0, mzz0,
                             b_x0, b_y0, b_z0)
            jac[i, 7] = jac8(v_x[i], v_y[i], v_z[i],
                             mxx0, mxy0, mxz0,
                             myy0, myz0, mzz0,
                             b_x0, b_y0, b_z0)
            jac[i, 8] = jac9(v_x[i], v_y[i], v_z[i],
                             mxx0, mxy0, mxz0, myy0, myz0, mzz0,
                             b_x0, b_y0, b_z0)
        r_new = np.linalg.norm(r_j)
        # Hessian matrix
        hes = np.linalg.pinv(np.dot(np.transpose(np.conj(jac)), jac))
        hes_non_inv = np.dot(np.transpose(np.conj(jac)), jac)
        des = np.dot(np.transpose(np.conj(jac)), r_j)
        des = np.transpose(np.conj(des))

#        v_k = v_k - np.dot(_lambda, np.dot(des, hes))
        v_k = v_k - np.dot(_lambda, (np.linalg.lstsq(hes_non_inv.T, des.T)[0].T))
        v_k = v_k.reshape(9, )
        print "Iteration num :" + str(k) + "\n" + str(v_k[0]) + " " + \
            str(v_k[1]) + " " + str(v_k[2]) + " " + str(v_k[3]) + " " + \
            str(v_k[4]) + " " + str(v_k[5]) + " " + str(v_k[6]) + " " + \
            str(v_k[7]) + " " + str(v_k[8]) + "\n" + "Error : " +str(r_new)

        # This is to make sure that the error is decreasing with every
        # iteration
        if r_new <= r_old:
            _lambda = _lambda - k_l * _lambda
        else:
            _lambda = k_l * _lambda

        # Iterations are stopped when the following convergence criteria is
        # satisfied
        if k > 1:
            print "Convergence tol. : " + str(np.abs(np.max(2 * (v_k - vold) / (v_k + vold)))) + "\n\n"
            if np.abs(np.max(2 * (v_k - vold) / (v_k + vold))) <= tol:
                print "Convergence achieved"
                break

        mxx0 = v_k[0]
        mxy0 = v_k[1]
        mxz0 = v_k[2]
        myy0 = v_k[3]
        myz0 = v_k[4]
        mzz0 = v_k[5]
        b_x0 = v_k[6]
        b_y0 = v_k[7]
        b_z0 = v_k[8]
        vold = v_k
        r_old = r_new

    if r_new > 2:
        print "Important error, WARNING : WRONG ACCELERATION CALIBRATION PARAMETERS"
        
        
    # Save Outputs
    scale = np.array([[v_k[0], v_k[1], v_k[2]], [v_k[1], v_k[3], v_k[4]],
                      [v_k[2], v_k[4], v_k[5]]])
    offset = np.transpose(np.array([v_k[6], v_k[7], v_k[8]]))

    return offset, scale


def errorf(v_x, v_y, v_z, mxx, mxy, mxz, myy, myz, mzz, b_x, b_y, b_z):
    """ error function given by Ax**2+Ay**2+Az**2 - g**2,
         where g = 9.81
    """
    val = (mxx * (b_x - v_x) + mxy * (b_y - v_y) + mxz * (b_z - v_z))**2 +\
          (mxy * (b_x - v_x) + myy * (b_y - v_y) + myz * (b_z - v_z))**2 +\
          (mxz * (b_x - v_x) + myz * (b_y - v_y) + mzz * (b_z - v_z))**2 - 9.81**2
    return val


def jac1(v_x, v_y, v_z, mxx, mxy, mxz, b_x, b_y, b_z):
    """ Functions jac1 to jac9 are the elements of the Jacobian
        vector (partial derivatives of the error function with
        respect to the gain and bias components)
    """
    val = 2 * (b_x - v_x)\
        * (mxx * (b_x - v_x) + mxy * (b_y - v_y) + mxz * (b_z - v_z))
    return val


def jac2(v_x, v_y, v_z, mxx, mxy, mxz, myy, myz, b_x, b_y, b_z):
    """ element 2 of the jacobian """
    val = 2 * (b_y - v_y)\
        * (mxx*(b_x - v_x) + mxy * (b_y - v_y) + mxz * (b_z - v_z))\
        + 2 * (b_x - v_x)\
        * (mxy * (b_x - v_x) + myy * (b_y - v_y) + myz * (b_z - v_z))
    return val


def jac3(v_x, v_y, v_z, mxx, mxy, mxz, myz, mzz, b_x, b_y, b_z):
    """ element 3 of the jacobian """
    val = 2 * (b_x - v_x)\
        * (mxz*(b_x - v_x) + myz * (b_y - v_y) + mzz * (b_z - v_z))\
        + 2*(b_z - v_z)\
        * (mxx * (b_x - v_x) + mxy * (b_y - v_y) + mxz * (b_z - v_z))
    return val


def jac4(v_x, v_y, v_z, mxy, myy, myz, b_x, b_y, b_z):
    """ element 4 of the jacobian """
    return 2*(b_y - v_y)*(mxy*(b_x - v_x) + myy*(b_y - v_y) + myz*(b_z - v_z))

def jac5(v_x, v_y, v_z, mxy, mxz, myy, myz, mzz, b_x, b_y, b_z):
    """ element 5 of the jacobian """
    val = 2*(b_y - v_y)*(mxz*(b_x - v_x) + myz*(b_y - v_y) + mzz*(b_z - v_z))\
        + 2*(b_z - v_z)*(mxy*(b_x - v_x) + myy*(b_y - v_y) + myz*(b_z - v_z))
    return val


def jac6(v_x, v_y, v_z, mxz, myz, mzz, b_x, b_y, b_z):
    """ element 6 of the jacobian """
    val = 2*(b_z - v_z)*(mxz*(b_x - v_x) + myz*(b_y - v_y) + mzz*(b_z - v_z))
    return val


def jac7(v_x, v_y, v_z, mxx, mxy, mxz, myy, myz, mzz, b_x, b_y, b_z):
    """ element 7 of the jacobian """
    val = 2*mxx*(mxx*(b_x - v_x) + mxy*(b_y - v_y) + mxz*(b_z - v_z))\
        + 2*mxy*(mxy*(b_x - v_x) + myy*(b_y - v_y) + myz*(b_z - v_z))\
        + 2*mxz*(mxz*(b_x - v_x) + myz*(b_y - v_y) + mzz*(b_z - v_z))
    return val


def jac8(v_x, v_y, v_z, mxx, mxy, mxz, myy, myz, mzz, b_x, b_y, b_z):
    """ element 8 of the jacobian """
    val = 2*mxy*(mxx*(b_x - v_x) + mxy*(b_y - v_y) + mxz*(b_z - v_z))\
        + 2*myy*(mxy*(b_x - v_x) + myy*(b_y - v_y) + myz*(b_z - v_z))\
        + 2*myz*(mxz*(b_x - v_x) + myz*(b_y - v_y) + mzz*(b_z - v_z))
    return val


def jac9(v_x, v_y, v_z, mxx, mxy, mxz, myy, myz, mzz, b_x, b_y, b_z):
    """ f9 function """
    val = 2*mxz*(mxx*(b_x - v_x) + mxy*(b_y - v_y) + mxz*(b_z - v_z))\
        + 2*myz*(mxy*(b_x - v_x) + myy*(b_y - v_y) + myz*(b_z - v_z))\
        + 2*mzz*(mxz*(b_x - v_x) + myz*(b_y - v_y) + mzz*(b_z - v_z))
    return val


def compute_simple(data):
    """ Compute IMU accelerometer calibration parameters

    Parameters :
    ------------
    data : numpy array of float
           data sensor in motion containing all the acquisition
           on three axis

    Returns
    -------
     offset : numpy array of float (dim=3)
              offset parameter
     scale  : numpy array of float (dim=3)
               scale parameters
    """
    offset = [0, 0, 0]
    norm_acc = algo.compute_norm(data)
    val_scale = scale_fit_norm(norm_acc, 9.81)
    scale = [val_scale, val_scale, val_scale]

    return scale, offset

