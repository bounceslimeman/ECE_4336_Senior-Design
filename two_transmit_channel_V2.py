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

desiredPhaseShift =  input("Please input the desired phase shift in degrees: ")

tx_lo = rx_lo                                  # Set transmit Frequency equal to recieve frequency which is 2.4 GHz 

tx_gain0 = -3                                  # Transmit gain set to -3 dB.
tx_gain1 = -3                                  # Transmit gain set to -3 dB.

fc0 = int(200e3)                               # Intermediate frequency for a carrier signal (200 kHz).
phase_cal = 0                           # Calibration phase offset in degrees.
num_scans = 80                                 # Number of scanning iterations.
Plot_Compass = False                            # Boolean flag indicating whether to plot compass-style visualization. Target line or waveform

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

sdr.tx_cyclic_buffer = True                    # ??? needed but I dont know why tbh


#Program Transmission

fs = int(sdr.sample_rate)                      # Sample rate
N = 2**16                                      # Number of samples
ts = 1 / float(fs)                             # Sampling period.
t = np.arange(0, N * ts, ts)                   # Array of time steps for each sample.

                                               # In-phase and quadrature-phase components of a sinusoidal signal (cosine and sine)

i0 = np.cos(2 * np.pi * t * fc0) * 2 ** 14     # I/Q data for transmit channel 0
q0 = np.sin(2 * np.pi * t * fc0) * 2 ** 14
iq0 = i0 + 1j * q0                             # Combined I/Q signal for channel 0

phase_shift = np.pi * (desiredPhaseShift / np.pi )

                                               # I/Q data for transmit channel 1 (could be the same or different)
i1 = np.cos(2 * np.pi * t * fc0 + phase_shift) * 2 ** 14     # Example signal for channel 1
q1 = np.sin(2 * np.pi * t * fc0 + phase_shift) * 2 ** 14
iq1 = i1 + 1j * q1                             # Combined I/Q signal for channel 1

sdr.tx([iq0, iq1])                             # Send data to both Tx channels (0 and 1)

#Frequency Bin Setup
xf = np.fft.fftfreq(NumSamples, ts)            # FFT frequency bins, shifted and scaled to MHz.
xf = np.fft.fftshift(xf) / 1e6

signal_start = int(NumSamples * (samp_rate / 2 + fc0 / 2) / samp_rate)    # Define the frequency range of interest based on fc0
signal_end = int(NumSamples * (samp_rate / 2 + fc0 * 2) / samp_rate)

def calcTheta(phase):  # Calculates the steering angle based on phase shift using the distance between antennas and the RF frequency.
    arcsin_arg = np.deg2rad(phase)*3E8/(2*np.pi*rx_lo*d)
    arcsin_arg = max(min(1, arcsin_arg), -1)
    calc_theta = np.rad2deg(np.arcsin(arcsin_arg))
    return calc_theta

def dbfs(raw_data):    # Converts raw IQ data into decibels full scale (dBFS) using FFT.
    NumSamples = len(raw_data)
    win = np.hamming(NumSamples)
    y = raw_data * win
    s_fft = np.fft.fft(y) / np.sum(win)
    s_shift = np.fft.fftshift(s_fft)
    s_dbfs = 20 * np.log10(np.abs(s_shift) / (2**11))
    return s_dbfs

# Data collection and scanning
max_gains = []

for i in range(20):
    data = sdr.rx()
    
for i in range(num_scans):  # This block performs multiple scans, adjusting the phase shift between Rx_0 and Rx_1, summing the signals, and finding the peak.
    data = sdr.rx()
    Rx_0 = data[0]
    Rx_1 = data[1]
    peak_sum = []
    delay_phases = np.arange(-180, 180, 2)
    for phase_delay in delay_phases:
        delayed_Rx_1 = Rx_1 * np.exp(1j * np.deg2rad(phase_delay + phase_cal))
        delayed_sum = dbfs(Rx_0 + delayed_Rx_1)
        peak_sum.append(np.max(delayed_sum[signal_start:signal_end]))
    peak_dbfs = np.max(peak_sum)
    max_gains.append(peak_dbfs)  # Store max gain for averaging
    peak_delay_index = np.where(peak_sum == peak_dbfs)
    peak_delay = delay_phases[peak_delay_index[0][0]]
    steer_angle = int(calcTheta(peak_delay))         # It calculates the steering angle based on the peak phase delay.
    
    # Depending on Plot_Compass, it either plots the phase shift vs. peak sum or shows a compass-style polar plot indicating the steering angle.
    if Plot_Compass == False:
        plt.plot(delay_phases, peak_sum)
        plt.axvline(x=peak_delay, color='r', linestyle=':')
        plt.text(-180, -26, f"Peak signal occurs with phase shift = {round(peak_delay,1)} deg")
        plt.text(-180, -28, f"If d={int(d*1000)}mm, then steering angle = {steer_angle} deg")
       
        max_gain = np.max(peak_sum)
        avg_max_gain = np.mean(max_gains)  # Calculate the average max gain
        plt.text(140, 0, f"Gain = {max_gain:.1f} dB\nAvg Gain = {avg_max_gain:.1f} dB", fontsize=10, ha='right', va='top')  # Display both max and avg gain
       
        plt.ylim(top=0, bottom=-30)
        plt.xlabel("phase shift [deg]")
        plt.ylabel("Rx0 + Rx1 [dBfs]")
        plt.title("Phase Shift vs. Peak Sum")
        plt.grid(True)
        plt.show()
    else:
        fig = plt.figure(figsize=(3, 3))
        ax = plt.subplot(111, polar=True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_thetamin(-90)
        ax.set_thetamax(90)
        ax.set_rlim(bottom=-20, top=0)
        ax.set_yticklabels([])
        ax.vlines(np.deg2rad(steer_angle), 0, -20)
        ax.text(np.deg2rad(steer_angle), -10, f"{steer_angle} deg", va='bottom', ha='center')
        plt.title("Steering Angle Indication")
        plt.show()

sdr.tx_destroy_buffer()  # Destroys the transmit buffer to clean up.
if i > 40:
    print('\a')  # Outputs a sound when done
