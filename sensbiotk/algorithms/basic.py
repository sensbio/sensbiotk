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
Basic algo for sensors data
"""

import numpy as np
from scipy import signal

# disabling pylint errors 'E1101' no-member, false positive from pylint
# pylint:disable=I0011,E1101


def find_peaks(sig_raw, min_peak_height, min_peak_distance, max_peak_distance):

    """ Find locations and peak values in a 1D numpy array,
        taking into account a minimal peak height, min distance
         and max distance.

    Parameters :
    ------------
    sig_raw : 1D numpy array of float
     signal input
    min_peak_height : float
     minimum height of the peak to detect
    min_peak_distance : integer
     minimal nb of samples between two consecutives peaks
    max_peak_distance : integer
     maximal nb of samples between two consecutives peaks

    Returns
    -------
    sig_raw[locs]  : numpy array of float
     detected peaks values
    locs : numpy array of float
     detected peaks locations

    """

    # find extremas location
    loc_extrema = signal.argrelextrema(sig_raw, np.greater)[0]
    dif_loc_extrema = np.diff(loc_extrema)
    # keeps only extremas between min and max_peak_distance spaced
    loc_extrema_dist = \
        loc_extrema[np.logical_and(
            dif_loc_extrema > min_peak_distance,
            dif_loc_extrema < max_peak_distance
            )]
    # keeps only extremas higher than the min peak threshold
    locs = loc_extrema_dist[
        np.nonzero(sig_raw[loc_extrema_dist] > min_peak_height)[0]
        ]
    return [sig_raw[locs], locs]


def find_static_periods(sig_raw, static_threshold, min_sample_duration):
    """ Find locations of static periods in a 1D numpy array, taking
    into account a minimal static threshold (ex: 3 deg/s), and a minimum
    nb of samples for the static duration.

    Parameters :
    ------------
    sig_raw : 1D numpy array of float
     signal input
    static_threshold : float
     threshold for considering a static period (ex: < deg/s)
    min_sample_duration : integer
     minimum nb of consecutives samples considered as
     a static period (duration * Fs)

    Returns
    -------
    start_idx  : numpy array of float
     start periods locations
    end_idx : numpy array of float
     end periods locations

    """
    temp = \
        np.concatenate([
            np.zeros(1),
            np.transpose(np.abs(sig_raw) < static_threshold),
            np.zeros(1)
            ])
    dtemp = np.diff([temp])
    # indices of start periods
    start_idx = (np.where(dtemp == 1))[1]
    # indices of end periods
    end_idx = (np.where(dtemp == -1))[1]
    count = end_idx - start_idx
    end_idx = end_idx - 1

    start_tab = start_idx[np.where(count >= min_sample_duration)]
    end_tab = end_idx[np.where(count >= min_sample_duration)]

    return [start_tab, end_tab]


def find_static_periods_3D(sig_raw, static_threshold, min_sample_duration):
    """ Find locations of static periods in a 3D numpy array, taking
    into account a minimal static threshold (ex: 3 deg/s), and a minimum
    nb of samples for the static duration.

    Parameters :
    ------------
    sig_raw : 3D numpy array of float
     signal input (ex: gyr(x,y,z))
    static_threshold : float
     threshold for considering a static period (ex: < deg/s)
    min_sample_duration : integer
     minimum nb of consecutives samples considered as
     a static period (duration * Fs)

    Returns
    -------
    start_idx  : numpy array of float
     start periods locations
    end_idx : numpy array of float
     end periods locations

    """
    temp = \
        np.concatenate([
            np.zeros(1),
            np.transpose(
            (np.abs(sig_raw[:, 0]) < static_threshold) & \
            (np.abs(sig_raw[:, 1]) < static_threshold) & \
            (np.abs(sig_raw[:, 2]) < static_threshold)),
            np.zeros(1)
            ])
    dtemp = np.diff([temp])
    # indices of start periods
    start_idx = (np.where(dtemp == 1))[1]
    # indices of end periods
    end_idx = (np.where(dtemp == -1))[1]
    count = end_idx - start_idx
    end_idx = end_idx - 1

    start_tab = start_idx[np.where(count >= min_sample_duration)]
    end_tab = end_idx[np.where(count >= min_sample_duration)]

    return [start_tab, end_tab]

def cut_signal(sig_time, sig_raw, time0, timef):
    """ Cut the signal on a windows between time0 and timef.

    Parameters :
    ------------
    sig_time : numpy array of float of dim N
    time signal
    sig_raw  : numpy array of float of dim Nx3
    signal
    time0    : float
    initial time of the window,
    timef    : float
    final time  of the window,

    Returns
    -------
    sig_time:numpy array of float
      time signal between time0 and timef
    sig_cut : numpy array of float
      signal cutted in a window time0 and timef.
    """
    tc_i = np.max(np.where(sig_time[:, 0] <= time0))
    tc_f = np.max(np.where(sig_time[:, 0] <= timef)) + 1

    print "TIME", tc_i, tc_f, time0, timef

    return [sig_time[tc_i:tc_f, :], sig_raw[tc_i:tc_f, 0:3]]


def lowpass_filter(sig_raw, cuttoff_freq, samp_freq):
    """ Low pass filter (butterworth order 6) on a signal

    Parameters :
    ------------
    sig_raw : numpy array of float of dim N
     signal to be filtered
    cuttoff_freq : float
     cut-off frequency
    samp_freq: float
     sampling frequency

    Returns
    -------
    sig_filt : numpy array of float of dim N
    signal filtered
    """
    norm_pass = cuttoff_freq / (samp_freq / 2)
    (param_b, param_a) = signal.butter(6, norm_pass)
    sig_filt = signal.filtfilt(param_b, param_a, sig_raw)

    return sig_filt


def lowpass_filter2(sig_raw, cuttoff_freq, samp_freq):
    """ Simple low pass filter on a signal

    Parameters :
    ------------
    sig_raw : numpy array of float of dim N
     signal to be filtered
    cuttoff_freq : float
     cut-off frequency
    samp_freq: float
     sampling frequency

    Returns
    -------
    sig_filt : numpy array of float of dim N
    signal filtered
    """
    vdt = 1 / samp_freq
    vrc = 1 / (2 * np.pi * cuttoff_freq)
    alpha = vdt / (vrc + vdt)

    print "ALPHA", alpha

    sig_filt = np.zeros(len(sig_raw))
    sig_filt[0] = sig_raw[0]
    for i in range(1, len(sig_raw)):
        sig_filt[i] = sig_filt[i-1] + alpha * (sig_raw[i] - sig_filt[i-1])

    return sig_filt


def window_mean(sig_time, sig_raw, time0, timef):
    """ Mean of the signal on a windows between time0 and timef.

    Parameters :
    ------------
    sig_time : numpy array of float
     time signal
    sig_raw  : numpy array of float of dim Nx3
     signal
    time0    : float
     initial time to compute the offset,
    timef    : float
     final time to compute the offset

    Returns
    -------
    sig_mean : numpy array of float
     mean of the signal assumed to be constant between time0 and timef.
    """
    tc_i = np.max(np.where(sig_time[:, 1] <= time0))
    tc_f = np.max(np.where(sig_time[:, 1] <= timef)) + 1

    print "TIME", tc_i, tc_f

    sig_mean = [np.mean(sig_raw[tc_i:tc_f, 0]),
                np.mean(sig_raw[tc_i:tc_f, 1]),
                np.mean(sig_raw[tc_i:tc_f, 2])]

    print "Signal Offset =", sig_mean

    return sig_mean


def moving_average(sig_raw, fen):
    """ Moving Average on a signal

    Parameters :
    ------------
    sig_raw : numpy array of float of dim N
    signal to be filtered
    fen  : size index  of the windows for the moving average

    Returns
    -------
    sig_filt : numpy array of float
    signal filtered
    """
    lensig = len(sig_raw)
    sig_filt = np.zeros(lensig)

    for i in range(lensig-fen):
        moy = 0.0
        for j in range(i, i + fen):
            moy = moy + sig_raw[j]
        sig_filt[i] = moy / fen

    for i in range(0, fen):
        sig_filt[i] = sig_raw[i]
    for i in range(lensig-fen, lensig):
        sig_filt[i] = sig_raw[i]

   # return sig_filt[fen-1:-fen+1]
    return sig_filt


def moving_average2(sig_raw, fen):
    """ Moving Average using convolution on a signal

    Parameters :
    ------------
    sig_raw : numpy array of float of dim N
    signal to be filtered
    fen  : size index  of the windows for the moving average

    Returns
    -------
    sig_filt : numpy array of float
    signal filtered
    """
    win = np.ones(fen, 'd')
    sig_filt = np.convolve(win/win.sum(), sig_raw, mode='same')

   # return sig_filt[fen-1:-fen+1]
    return sig_filt


def search_maxpeak(sig_raw):
    """ Search max peak

    Parameters :
    ------------
    sig_time: numpy array of float of dim N
     signal time
    sig_raw : numpy array of float of dim N
     signal input

    Returns
    -------
    time_peak  : numpy array of float
       time where a max peak has been detected
    index_peak : numpy array of float
        index where a max peak has been detected

    """
    index_peak = (np.diff(np.sign(np.diff(sig_raw))) < 0).nonzero()[0] + 1
   # index_peak = signal.argrelmax(sig_raw, np.greater)

    return index_peak


def threshold_signal(sig_time, sig_raw, threshold):
    """ Threshold signal

    Parameters :
    ------------
    sig_time: numpy array of float of dim N
     signal time
    sig_raw : numpy array of float of dim N
     signal input
    threshold : float
     threshold for the signal

    Returns
    -------
    time_thresh  : numpy array of float
     time signal thresholed
    index_peak : numpy array of float
     signal thresholed
    """

    acc_thresh = sig_raw[sig_raw > threshold]
    time_thresh = sig_time[np.where(sig_raw > threshold)]

    return [time_thresh, acc_thresh]


def threshold_under_signal(sig_time, sig_raw, threshold):
    """ Threshold under signal

    Parameters :
    ------------
    sig_time: numpy array of float of dim N
     signal time
    sig_raw : numpy array of float of dim N
     signal input
    threshold : float
     threshold for the signal

    Returns
    -------
    time_thresh  : numpy array of float
     time signal thresholed
    index_peak : numpy array of float
     signal thresholed
    """

    acc_thresh = sig_raw[sig_raw < threshold]
    time_thresh = sig_time[np.where(sig_raw < threshold)]

    return [time_thresh, acc_thresh]



def compute_norm(sig_raw):
    """ Norm on a signal

    Parameters :
    ------------
    sig_raw : numpy array of float of dim Nx3
     signal to be normed

    Returns
    -------
    sig_norm : numpy array of float
     norm of the signal
    """
    sig_norm = np.sqrt(np.sum(sig_raw[:, i]**2 for i in range(0, 3)))

    return sig_norm

