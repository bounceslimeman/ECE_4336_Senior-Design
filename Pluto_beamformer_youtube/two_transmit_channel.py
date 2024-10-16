"""
modified from https://github.com/analogdevicesinc/pyadi-iio/blob/ensm-example/examples/pluto.py
"""
# Copyright (C) 2020 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import time
import matplotlib.pyplot as plt
import numpy as np
import adi

# Create radio
sdr = adi.ad9361(uri='ip:192.168.2.1')  #adi.ad9361(uri='ip:192.168.2.2') for the other pluto

# Does this ip address need to be different with two plutos talking to each other?
samp_rate = 30.72e6    # must be <=30.72 MHz if both channels are enabled
#do this for both 

num_samps = 2**18      # number of samples per buffer.  Can be different for Rx and Tx
# would reducing or inreasing the sample rate   cause any processing issues?
# 32.768 kilobytes per sample

rx_lo = 2.4e9 # receive at 2.4 gigahertz 

rx_mode = "slow_attack"  # can be "manual" or "slow_attack"
# what does manual mode on the pluto do? - manual turns on the ADC, we dont want that

rx_gain0 = 10
# 10 what?
rx_gain1 = 10
# 10 what?
tx_lo = rx_lo
#the transmit frequency is the same the the recieve frequency  
tx_gain0 = -10
# 10 what? why negative?
tx_gain1 = -10
# 10 what? why negative? - 

#what is the gains, why is transmit negative and why is recieve positive, if the two channels
#are not directly connected does this change anything?


'''Configure Rx properties'''
sdr.rx_enabled_channels = [0, 1]
# is what does the array specify? the channels used? 
#and can we choose to do specific things with specific channels?
# does a sdr.tx_enable_channels exist? 

#Same as before "
sdr.sample_rate = int(samp_rate)
sdr.rx_lo = int(rx_lo)
sdr.gain_control_mode = rx_mode
sdr.rx_hardwaregain_chan0 = int(rx_gain0)
sdr.rx_hardwaregain_chan1 = int(rx_gain1)
sdr.rx_buffer_size = int(num_samps) 
#"

'''Configure Tx properties'''

sdr.tx_enabled_channels = [0, 1] # new channel enables

sdr.tx_rf_bandwidth = int(samp_rate)
sdr.tx_lo = int(tx_lo)
sdr.tx_cyclic_buffer = True
sdr.tx_hardwaregain_chan0 = int(tx_gain0)
sdr.tx_hardwaregain_chan1 = int(tx_gain1)
sdr.tx_buffer_size = int(num_samps)

# Example read properties
print("RX LO %s" % (sdr.rx_lo))

# Program the Tx with some data
fs = int(sdr.sample_rate)
fc0 = int(2e6)
fc1 = int(5e6)
N = 2**16
ts = 1 / float(fs)
t = np.arange(0, N * ts, ts)
i0 = np.cos(2 * np.pi * t * fc0) * 2 ** 14
q0 = np.sin(2 * np.pi * t * fc0) * 2 ** 14
i1 = np.cos(2 * np.pi * t * fc1) * 2 ** 14
q1 = np.sin(2 * np.pi * t * fc1) * 2 ** 14
iq0 = i0 + 1j * q0
iq1 = i1 + 1j * q1
sdr.tx([iq0, iq1])   # Send Tx data.

# Collect data
for r in range(20):    # grab several buffers to give the AGC time to react (if AGC is set to "slow_attack" instead of "manual")
    data = sdr.rx()



