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
Martin Salaun observer implementation

This algorithms is based on the following work :

Martin, P. and E. Salaün, Design and implementation
of a low-cost observer-based attitude and heading reference system.
Control Engineering Practice, 2010. 18(7): p. 712-722.

It enables the computation of a quaternion from magneto-inertial measurements.

The provided quaternion is expressed regarding the NED (North East Down) frame.
Once the observer initialized, please take note that the algorithm needs few seconds
to converge toward its correct attitude and heading.


"""

# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,C0103
# disabling pylint errors 'E1101' no-member, false positive from pylint
# pylint:disable=I0011,E1101

import numpy as np
from sensbiotk.transforms3d import quaternions as nq


class martin_ahrs(object):
    """
    Martin Salaun observer class
    """
    def __init__(self):

#        # Observer gains (test)
#        self.la = 0.06
#        self.lc = 0.1
#        self.ld = 0.06
#        self.n = 0.25
#        self.o = 0.50
#        self.k = 1
#        self.sigma = 4./75
#        # Gravity scale factor
#        self.a_s = 9.81
#        # Magnetic field scale factor
#        self.c_s =  self.a_s*1

        # Observer gains (HikoB)
        self.la = 0.7
        self.lc = 0.1
        self.ld = 0.01
        self.n = 0.01
        self.o = 0.01
        self.k = 0.7
        self.sigma = 0.002
        # Gravity scale factor
        self.a_s = 9.81
        # Magnetic field scale factor
        self.c_s = self.a_s*1
        # Reconstructed quaternion
        self.q = [1.0, 0.0, 0.0, 0.0]
        self.qinv = [1.0, 0.0, 0.0, 0.0]
        self.wb = [0.0, 0.0, 0.0, 0.0]
        # Quaternion director
        self._A = [0.0, 0.0, 0.0, 1.0]
        self._C = [0.0, 0.0, 1.0, 0.0]
        self._D = [0.0, 1.0, 0.0, 0.0]

        return

    def init_observer(self, z):
        """ Martin Salaun init observer
        """
        # Quaternions construction
        ya = [0, z[0], z[1], z[2]]
        yb = [0, z[3], z[4], z[5]]
        yc = nq.mult(ya, yb)
        # Normalization
        ya = nq.normalize(ya)
#        yb = nq.normalize(yb)
        yc[0] = 0
        yc = nq.normalize(yc)

        if ya[3] == 1:
            self.q = 1
            self.qinv = 1
        else:
            self.qinv = [-ya[2], 1 - ya[3], 0, ya[1]]
            self.qinv = nq.normalize(self.qinv)
            self.q = nq.conjugate(self.qinv)

        yc = nq.mult(nq.mult(self.q, yc), self.qinv)

        if yc[2] != 1:
            self.qinv = nq.mult(self.qinv, [-yc[1], 0, yc[3], 1 - yc[2]])
            self.qinv = nq.normalize(self.qinv)
            self.q = nq.conjugate(self.qinv)

        return self.q

    def update(self, z, sample_period):
        """ Martin Salaun iteration observer
        """

        # Quaternions construction
        ya = np.array([0, z[0], z[1], z[2]])
#        ya = nq.normalize(ya)
        yb = np.array([0, z[3], z[4], z[5]])
#        yb = nq.normalize(yb)
        wm = np.array([0, z[6], z[7], z[8]])
#        wm = nq.normalize(wm)

        # Compute quaternions products
        yc = nq.mult(ya, yb)
        yc[0] = 0
        yd = nq.mult(yc, ya)
        yd[0] = 0

        # Compute errors
        EA = self._A - \
            nq.mult(self.q, nq.mult(ya, self.qinv)) / self.a_s
        EC = self._C - \
            nq.mult(self.q, nq.mult(yc, self.qinv)) / self.c_s
        ED = self._D - \
            nq.mult(self.q, nq.mult(yd, self.qinv)) / (self.a_s * self.c_s)

        # Numerical stabilisation
        EA[0] = 0
        EC[0] = 0
        ED[0] = 0

        # sEA = <EA, EA - A> = ||EA||² - <EA, A>
        sEA = nq.norm(EA) - EA[3]
        # sEC = <EC, EC - C> = ||EC||² - <EC, C>
        sEC = nq.norm(EC) - EC[2]
        # sED = <ED, ED - D> = ||ED||² - <ED, D>
        sED = nq.norm(ED) - ED[1]

        LE = nq.mult(self._A, EA) * self.la + nq.mult(self._C, EC) * self.lc \
            + nq.mult(self._D, ED) * self.ld
        LE[0] = 0
        ME = LE * (-self.sigma)

        if self.la + self.ld != 0:
            NE = self.n / (self.la + self.ld) * (self.la * sEA + self.ld * sED)
        else:
            NE = 0

        if self.lc + self.ld != 0:
            OE = self.o / (self.lc + self.ld) * (self.lc * sEC + self.ld * sED)
        else:
            OE = 0

        qdot = nq.mult(self.q, wm - self.wb) * 0.5 + \
            nq.mult(LE, self.q) + self.q * (self.k * (1 - nq.norm(self.q)))
        wbdot = nq.mult(nq.mult(self.qinv, ME), self.q)
        a_sdot = self.a_s * NE
        csdot = self.c_s * OE

        # Integration
        self.q = self.q + qdot * sample_period
        self.wb = self.wb + wbdot * sample_period
        self.a_s = self.a_s + a_sdot * sample_period
        self.c_s = self.c_s + csdot * sample_period

        # compute inverse for the next step
        self.qinv = nq.conjugate(self.q)

        qrot = nq.mult([0, 1, 0, 0], self.q)

        return qrot

