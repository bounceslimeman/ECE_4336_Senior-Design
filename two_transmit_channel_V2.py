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

tx_gain0 = -3                                  # Transmit gain set to -3 dB.
tx_gain1 = -3                                  # Transmit gain set to -3 dB.

fc0 = int(200e3)                               # Intermediate frequency for a carrier signal (200 kHz).
phase_cal = 0                                  # Calibration phase offset in degrees.
num_scans = 80                                 # Number of scanning iterations.
Plot_Compass = True                            # Boolean flag indicating whether to plot compass-style visualization. Target line or waveform

d_wavelength = 0.5                             # Distance between receive antennas as a fraction of the wavelength (0.5). distance was designed around wavelength
wavelength = 3E8/rx_lo                         # Compute the wavelength of the RF carrier using the speed of light (3 × 10^8 m/s) divided by rx_lo. 

d = d_wavelength*wavelength                    # Physical distance between the receive antennas in meters.

#SDR Configuration 

sdr = adi.ad9361(uri='ip:192.168.2.1')         # Initializes the AD9361 radio, using the IP address of the device, change the last number to 2 when writting code for the other SDR
sdr.rx_enabled_channels = [0, 1]               # Enables both recieve channels of the SDR
sdr.tx_enabled_channels = [0, 1]               # Enables both transmit channels of the SDR
sdr.sample_rate = int(samp_rate)               # Sets sample rate based on given sample rate variable

sdr.rx_rf_bandwidth = int(fc0 * 3)             # sets recieve radio frequency bandwidth at carrier frequency times 3 
sdr.rx_lo = int(rx_lo)                         # Sets recieve frequency to to chosen recieve value 
sdr.tx_rf_bandwidth = int(fc0 * 3)             # sets transmit radio frequency bandwidth at carrier frequency times 3 
sdr.tx_lo = int(tx_lo)                         # sets transmit frequency to chosen recieve value

sdr.gain_control_mode = rx_mode                # sets the control mode to chosen variable which is manual 

sdr.rx_hardwaregain_chan0 = int(rx_gain0)      # sets the various gain values to their previously chosen values
sdr.rx_hardwaregain_chan1 = int(rx_gain1)
sdr.tx_hardwaregain_chan0 = int(tx_gain0)
sdr.tx_hardwaregain_chan1 = int(tx_gain1)


sdr.rx_buffer_size = int(NumSamples)           # buffer for recieving equals the number of samples we want
sdr.tx_buffer_size = int(2**18)                # buffer for trasmitting set at 262144 bits 

sdr._rxadc.set_kernel_buffers_count(1)         # Reduces buffers to avoid stale data.








