# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:18:38 2024

@author: bounc
"""

import adi                                     # Pluto SDR proprietary Library
import matplotlib.pyplot as plt                # data plottting library
import numpy as np                             # math functions library


#Setup Parameters
samp_rate = 2e6                                # The sample rate of the radio (2 MHz).
NumSamples = 2**12                             # Number of samples per buffer (4096). 2^12
rx_lo = 2.4e9                                  # Receive Local Oscillator frequency (2.4 GHz)
rx_mode = "manual"                             # Gain control mode for the receiver, set to manual.
rx_gain0 = 40                                  # Receive gains for channels 0 and 1.
rx_gain1 = 40

tx_lo = rx_lo                                  # Set transmit Frequency equal to recieve frequency which is 2.4 GHz 

tx_gain = -3                                   # Transmit gain set to -3 dB.
fc0 = int(200e3)                               # Intermediate frequency for a carrier signal (200 kHz).
phase_cal = 0                                  # Calibration phase offset in degrees.
num_scans = 80                                 # Number of scanning iterations.
Plot_Compass = True                            # Boolean flag indicating whether to plot compass-style visualization. Target line or waveform

d_wavelength = 0.5                             # Distance between receive antennas as a fraction of the wavelength (0.5). distance was designed around wavelength
wavelength = 3E8/rx_lo                         # Compute the wavelength of the RF carrier using the speed of light (3 × 10^8 m/s) divided by rx_lo. 

